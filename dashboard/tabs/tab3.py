import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils.dataloader import load_feature_importance, load_shap_data

def render(battery_id, model_type, preprocessing):
    if model_type != "LOF":
        st.warning("⚠️ Feature Importance는 LOF 모델에서만 제공됩니다.")
        st.info("왼쪽 사이드바에서 **LOF** 모델을 선택해주세요.")
        return  # stop() → return
    
    st.subheader("Feature Importance & Interpretability")
    
    # 데이터 로드 (함수 사용)
    feature_importance = load_feature_importance(battery_id, preprocessing)
    shap_values, X_explain = load_shap_data(battery_id, preprocessing)
    
    features = feature_importance['feature'].tolist()
    importance_scores = feature_importance['importance'].tolist()
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.metric("Most Important", features[0])
    with col2:
        st.metric("Importance Score", f"{importance_scores[0]:.4f}")
    
    st.markdown("---")
    
    # 1. Feature Importance 가로 막대
    st.markdown("### Feature Contribution to Anomaly Detection")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        top_n = st.selectbox("Show Top N Features", [5, 10, len(features)], index=1)
    
    # 색상 그라데이션
    threshold_high = np.percentile(importance_scores[:top_n], 66)
    threshold_mid = np.percentile(importance_scores[:top_n], 33)
    
    colors = ['darkred' if s > threshold_high else 'orange' if s > threshold_mid else 'steelblue' 
              for s in importance_scores[:top_n]]
    
    fig_importance = go.Figure()
    fig_importance.add_trace(go.Bar(
        y=features[:top_n][::-1],
        x=importance_scores[:top_n][::-1],
        orientation='h',
        marker=dict(color=colors[::-1]),
        text=[f"{s:.4f}" for s in importance_scores[:top_n][::-1]],
        textposition='outside'
    ))
    
    fig_importance.update_layout(
        xaxis_title="Importance Score (mean |SHAP value|)",
        yaxis_title="",
        height=max(400, top_n * 40),
        showlegend=False,
        margin=dict(l=0, r=50, t=10, b=30)
    )
    
    st.plotly_chart(fig_importance, use_container_width=True)
    
    st.markdown("---")
    
    # 2. SHAP Value Distribution
    st.markdown("### SHAP Value Analysis")
    
    top_features_for_swarm = features[:10]
    
    fig_swarm = go.Figure()
    
    for i, feat in enumerate(top_features_for_swarm):
        if feat in X_explain.columns:
            feature_values = X_explain[feat].values
            feat_idx = features.index(feat)
            shap_vals = shap_values[:, feat_idx]
            
            fig_swarm.add_trace(go.Scatter(
                x=feature_values,
                y=[feat] * len(feature_values),
                mode='markers',
                name=feat,
                marker=dict(
                    color=shap_vals,
                    colorscale='RdBu_r',
                    size=8,
                    opacity=0.6,
                    showscale=(i == 0),
                    colorbar=dict(title="SHAP value") if i == 0 else None
                ),
                showlegend=False
            ))
    
    fig_swarm.update_layout(
        xaxis_title="Feature Value",
        yaxis_title="",
        height=500,
        hovermode='closest'
    )
    
    st.plotly_chart(fig_swarm, use_container_width=True)
    
    # Feature 설명
    with st.expander("📖 Feature 설명"):
        st.markdown("""
        ### 주요 Feature 설명
        
        - **Current_measured_trend**: 측정 전류의 추세 성분 (장기 변화 패턴)
        - **Current_load_trend**: 부하 전류의 추세 성분
        - **Voltage_measured_trend**: 측정 전압의 추세 성분
        - **Voltage_load_trend**: 부하 전압의 추세 성분
        - **Temperature_measured**: 실측 온도값
        - **Temperature_measured_smooth**: 평활화된 온도 데이터
        - **Temperature_measured_residual**: 온도 잔차 (이상 변동)
        - **Voltage_measured**: 실측 전압값
        - **Voltage_measured_smooth**: 평활화된 전압 데이터
        - **Current_load_smooth**: 평활화된 부하 전류
        
        **_trend**: LOWESS 등으로 추출한 장기 추세  
        **_smooth**: Moving average 등 평활화  
        **_residual**: 원본 - 평활 = 노이즈/이상 신호
        """)
