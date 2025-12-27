# main.py
import streamlit as st
import sys
import os

# 현재 폴더를 Python 경로에 추가
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from tabs import tab1 as tab1_module
from tabs import tab2 as tab2_module
from tabs import tab3 as tab3_module
from tabs import tab4 as tab4_module
from tabs import tab5 as tab5_module

# Page config
st.set_page_config(
    page_title="Battery Anomaly Detection Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.title("⚡ Battery Anomaly Detection")
    
    battery_id = st.selectbox(
        "Select Battery",
        ["B0005", "B0006", "B0007"]
    )
    
    st.markdown("---")
    
    st.subheader("Model Configuration")
    model_type = st.radio(
        "Model Type",
        ["Anomaly Transformer", "LOF"]
    )
    
    st.markdown("---")
    st.subheader("Select Dataset Type")
    preprocessing = st.radio(
        "Preprocessing",
        ["LOWESS", "Raw Data"]
    )
    
    st.markdown("---")
    
    if st.button("🔄 Refresh Analysis", use_container_width=True):
        st.rerun()

# Main title
st.title("🔋 Battery Health Monitoring Dashboard")
st.markdown(f"**Dataset:** NASA PCoE Battery Dataset - {battery_id}")

def get_metrics(model_type, preprocessing, battery_id):
    """모델/전처리에 따른 메트릭 반환"""
    
    if model_type == "Anomaly Transformer" and preprocessing == "LOWESS" and battery_id == "B0005":
        return {
            'capacity_corr': "-0.747",
            'rohmic_corr': "+0.641",
            'anomaly_cycle': "Cycle 485",
            'capacity_delta': "-22.9% vs baseline",
            'rohmic_delta': "-32.7% vs baseline",
            'p_value': "< 0.01",
            'confidence': 'High Confidence'
        }
    elif model_type == "Anomaly Transformer" and preprocessing == "Raw Data" and battery_id == "B0005":
        return {
            'capacity_corr': "-0.423",
            'rohmic_corr': "+0.312",
            'anomaly_cycle': "Cycle 485",
            'capacity_delta': "-49.9% vs baseline",
            'rohmic_delta': "-62.9% vs baseline",
            'p_value': "> 0.05",
            'confidence': 'Low Confidence'
        }
    elif model_type == "LOF" and preprocessing == "LOWESS" and battery_id == "B0005":
        return {
            'capacity_corr': "-0.973",
            'rohmic_corr': "+0.952",
            'anomaly_cycle': "Cycle 437",
            'capacity_delta': "baseline",
            'rohmic_delta': "baseline",
            'p_value': "< 0.01",
            'confidence': 'High Confidence'
        }
    elif model_type == "LOF" and preprocessing == "Raw Data" and battery_id == "B0005":
        return {
            'capacity_corr': "-0.845",
            'rohmic_corr': "+0.844",
            'anomaly_cycle': "Cycle 589",
            'capacity_delta': "baseline",
            'rohmic_delta': "baseline",
            'p_value': "< 0.01",
            'confidence': 'High Confidence'
        }
    elif model_type == "Anomaly Transformer" and preprocessing == "LOWESS" and battery_id == "B0006":
        return {
            'capacity_corr': "-0.536",
            'rohmic_corr': "+0.331",
            'anomaly_cycle': "Cycle 485",
            'capacity_delta': "% vs baseline",
            'rohmic_delta': "% vs baseline",
            'p_value': "< 0.01",
            'confidence': 'High Confidence'
        }
    elif model_type == "Anomaly Transformer" and preprocessing == "Raw Data" and battery_id == "B0006":
        return {
            'capacity_corr': "-0.643",
            'rohmic_corr': "+0.741",
            'anomaly_cycle': "Cycle 485",
            'capacity_delta': "% vs baseline",
            'rohmic_delta': "% vs baseline",
            'p_value': "> 0.05",
            'confidence': 'Low Confidence'
        }
    elif model_type == "LOF" and preprocessing == "LOWESS" and battery_id == "B0006":
        return {
            'capacity_corr': "-0.912",
            'rohmic_corr': "+0.854",
            'anomaly_cycle': "Cycle 437",
            'capacity_delta': "baseline",
            'rohmic_delta': "baseline",
            'p_value': "< 0.01",
            'confidence': 'High Confidence'
        }
    elif model_type == "LOF" and preprocessing == "Raw Data" and battery_id == "B0006":
        return {
            'capacity_corr': "-0.789",
            'rohmic_corr': "+0.712",
            'anomaly_cycle': "Cycle 589",
            'capacity_delta': "baseline",
            'rohmic_delta': "baseline",
            'p_value': "< 0.05",
            'confidence': 'Medium Confidence'
        }
    elif model_type == "Anomaly Transformer" and preprocessing == "LOWESS" and battery_id == "B0007":
        return {
            'capacity_corr': "-0.738",
            'rohmic_corr': "+0.674",
            'anomaly_cycle': "Cycle 485",
            'capacity_delta': "% vs baseline",
            'rohmic_delta': "% vs baseline",
            'p_value': "< 0.01",
            'confidence': 'High Confidence'
        }
    elif model_type == "Anomaly Transformer" and preprocessing == "Raw Data" and battery_id == "B0007":
        return {
            'capacity_corr': "+0.220",
            'rohmic_corr': "-0.01",
            'anomaly_cycle': "Cycle 485",
            'capacity_delta': "% vs baseline",
            'rohmic_delta': "% vs baseline",
            'p_value': "> 0.05",
            'confidence': 'Low Confidence'
        }
    elif model_type == "LOF" and preprocessing == "LOWESS" and battery_id == "B0007":
        return {
            'capacity_corr': "-0.887",
            'rohmic_corr': "+0.799",
            'anomaly_cycle': "Cycle 437",
            'capacity_delta': "baseline",
            'rohmic_delta': "baseline",
            'p_value': "< 0.01",
            'confidence': 'High Confidence'
        }
    elif model_type == "LOF" and preprocessing == "Raw Data" and battery_id == "B0007":
        return {
            'capacity_corr': "-0.765",
            'rohmic_corr': "+0.689",
            'anomaly_cycle': "Cycle 589",
            'capacity_delta': "baseline",
            'rohmic_delta': "baseline",
            'p_value': "< 0.05",
            'confidence': 'Medium Confidence'
        }
    else:
        # 기본값 반환
        return {
            'capacity_corr': "N/A",
            'rohmic_corr': "N/A",
            'anomaly_cycle': "N/A",
            'capacity_delta': "No data",
            'rohmic_delta': "No data",
            'p_value': "N/A",
            'confidence': 'No data'
        }

# Metrics row
col1, col2, col3, col4 = st.columns(4)

metrics = get_metrics(model_type, preprocessing, battery_id)

with col1:
    st.metric(
        label="Capacity Spearman Correlation",
        value=metrics['capacity_corr'],
        delta=metrics['capacity_delta']
    )

with col2:
    st.metric(
        label="R_ohmic Spearman Correlation",
        value=metrics['rohmic_corr'],
        delta=metrics['rohmic_delta']
    )

with col3:
    st.metric(
        label="Anomaly Detected",
        value=metrics['anomaly_cycle'],
        delta=metrics['confidence']
    )

with col4:
    st.metric(
        label="P-value",
        value=metrics['p_value'],
        delta="Statistically Significant" if "<" in metrics['p_value'] else "Not Significant"
    )

st.markdown("---")

# Main visualization area
overview_tab, anomaly_tab, feature_tab, health_tab, corr_tab = st.tabs(["📊 Overview", "🎯 Anomaly Scores", "🧩 Feature Importance", "💚 Health Indicator", "🔬 Correlation Analysis"])


with overview_tab:
    tab1_module.render(battery_id)

with anomaly_tab:
    tab2_module.render(battery_id, model_type, preprocessing)

with feature_tab:
    tab3_module.render(battery_id, model_type, preprocessing)

with health_tab:
    tab4_module.render(battery_id, model_type, preprocessing)

with corr_tab:
    tab5_module.render(battery_id, model_type, preprocessing)