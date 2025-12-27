import os
import pandas as pd
import pickle
import json
import boto3
import streamlit as st
from pathlib import Path

# S3 설정
S3_BUCKET = "dh-bucket-111"  # 실제 버킷명으로 변경
S3_PREFIX = "dataset/"  # S3에 업로드한 경로

def download_from_s3():
    """S3에서 dataset 폴더 전체 다운로드 (최초 1회만)"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local_dir = Path(base_dir) / "dataset"
    
    # 이미 다운로드되어 있으면 스킵
    if local_dir.exists() and any(local_dir.iterdir()):
        return
    
    local_dir.mkdir(exist_ok=True)
    
    # AWS credentials from Streamlit Secrets
    s3 = boto3.client(
        's3',
        aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
        region_name=st.secrets.get("AWS_REGION", "us-east-1")
    )
    
    # S3에서 모든 파일 다운로드
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=S3_PREFIX):
        for obj in page.get('Contents', []):
            s3_key = obj['Key']
            if s3_key == S3_PREFIX:  # 폴더 자체는 스킵
                continue
            local_path = local_dir / s3_key.replace(S3_PREFIX, '')
            local_path.parent.mkdir(parents=True, exist_ok=True)
            s3.download_file(S3_BUCKET, s3_key, str(local_path))

# 앱 시작 시 S3에서 데이터 다운로드
download_from_s3()

def get_base_dir():
    """프로젝트 루트 디렉토리 반환"""
    # data_loader.py 위치 기준으로 상위 폴더 (dashboard/)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_discharge_summary():
    """방전 요약 데이터 로드"""
    base_dir = get_base_dir()
    file_path = os.path.join(base_dir, 'dataset', 'discharge_summary.csv')
    return pd.read_csv(file_path)

def load_feature_importance(battery_id, preprocessing):
    """Feature Importance 데이터 로드"""
    base_dir = get_base_dir()
    
    if preprocessing == "LOWESS":
        filename = f'lof_{battery_id}_feature_importance_lowess.csv'
    else:
        filename = f'lof_{battery_id}_feature_importance.csv'
    
    file_path = os.path.join(base_dir, 'dataset', 'tab3', filename)
    
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}") from e

def load_anomaly_results(battery_id, model_type, preprocessing):
    """Anomaly Transformer 결과 로드"""

    base_dir = get_base_dir()

    if model_type != "Anomaly Transformer":
        return None
    
    if preprocessing == "LOWESS":
        filename = f'test_results_{battery_id}_lowess.pkl'
    else:
        filename = f'test_results_{battery_id}.pkl'
    
    file_path = os.path.join(base_dir, 'dataset', 'tab2', filename)
    
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}") from e

def load_shap_data(battery_id, preprocessing):
    """SHAP 분석 데이터 로드"""
    base_dir = get_base_dir()
    
    if preprocessing == "LOWESS":
        shap_file = f'shap_values_{battery_id}_lowess.npy'
        explain_file = f'X_test_explain_{battery_id}_lowess.csv'
    else:
        shap_file = f'shap_values_{battery_id}.npy'
        explain_file = f'X_test_explain_{battery_id}.csv'
    
    import numpy as np

    shap_path = os.path.join(base_dir, 'dataset', 'tab3', shap_file)
    explain_path = os.path.join(base_dir, 'dataset', 'tab3', explain_file)
    
    try:
        shap_values = np.load(shap_path)
        X_explain = pd.read_csv(explain_path)
        return shap_values, X_explain
    except FileNotFoundError as e:
        raise FileNotFoundError(f"SHAP 데이터를 찾을 수 없습니다: {e}") from e
    
def load_lof_cycle_summary(battery_id, preprocessing):
       """LOF 사이클 요약 데이터 로드"""
       suffix = "_lowess" if preprocessing == "LOWESS" else ""
       df = pd.read_csv(f'dataset/tab2/lof_{battery_id}_cycle_summary{suffix}.csv')
       
       with open(f'dataset/tab2/lof_{battery_id}_metadata{suffix}.json') as f:
           metadata = json.load(f)
       
       return df, metadata['threshold']

def load_hi_analysis(battery_id, preprocessing):
    """HI 변동성 분석 데이터 로드"""
    import json
    
    suffix = "_lowess" if preprocessing == "LOWESS" else ""
    val_test_df = pd.read_csv(f'dataset/tab4/{battery_id}_hi_analysis{suffix}.csv')

    with open(f'dataset/tab4/{battery_id}_hi_metadata{suffix}.json') as f:
        metadata = json.load(f)
    
    return val_test_df, metadata

def load_correlation_data(battery_id, model_type, preprocessing):
    """Correlation 분석 데이터 로드"""
    import json
    
    model_name = "at" if model_type == "Anomaly Transformer" else "lof"
    suffix = "_lowess" if preprocessing == "LOWESS" else ""
    
    df_merged = pd.read_csv(f'dataset/tab5/{battery_id}_correlation_{model_name}{suffix}.csv')

    if 'cycle_idx' in df_merged.columns:
        df_merged = df_merged.rename(columns={'cycle_idx': 'cycle'})

    with open(f'dataset/tab5/{battery_id}_correlation_metadata_{model_name}{suffix}.json') as f:
        metadata = json.load(f)
    
    return df_merged, metadata