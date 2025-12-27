import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.dataloader import load_hi_analysis

def render(battery_id, model_type, preprocessing):

    if model_type != "LOF":
        st.warning("⚠️ HI 지표는 LOF 모델에서만 제공됩니다.")
        st.info("왼쪽 사이드바에서 **LOF** 모델을 선택해주세요.")
        return  # stop() → return
    
    if preprocessing == "Raw Data":
        st.warning("⚠️ HI 지표는 Lowess 데이터에서만 제공됩니다.")
        st.info("왼쪽 사이드바에서 **Lowess** 데이터를 선택해주세요.")
        return  # stop() → return
    
    # 데이터 로드
    val_test_df, metadata = load_hi_analysis(battery_id, preprocessing)
    
    # 메타데이터 추출
    val_start = metadata['val_start']
    test_start = metadata['test_start']
    stable_threshold = metadata['stable_threshold']
    first_event = metadata.get('first_event')

    # 통계 요약
    st.subheader("Statistical Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Stable Threshold", f"{metadata['stable_threshold']:.6f}")
    with col2:
        st.metric("Early Phase HI Volatility", f"{metadata['early_hi_mean']:.6f}")
    with col3:
        st.metric("Late Phase HI Volatility", f"{metadata['late_hi_mean']:.6f}")

    st.markdown("---")
    
    st.subheader("Health Indicator Variability Analysis")

    # 시각화
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=(
            'HI_ema',
            'HI Absolute Change',
            'HI Slope Volatility'
        ),
        vertical_spacing=0.12
    )
    
    # Row 1: HI_ema
    fig.add_trace(
        go.Scatter(x=val_test_df['cycle_idx'], y=val_test_df['HI_ema'],
                   name='HI_ema', line=dict(color='blue', width=2)),
        row=1, col=1
    )
    
    # Row 2: HI 절댓값
    fig.add_trace(
        go.Scatter(x=val_test_df['cycle_idx'], y=val_test_df['HI_abs_change'],
                   name='HI Absolute Change', line=dict(color='purple', width=2)),
        row=2, col=1
    )
    
    # Row 3: HI 변동성
    fig.add_trace(
        go.Scatter(x=val_test_df['cycle_idx'], y=val_test_df['HI_slope_rollstd'],
                   name='HI Volatility', line=dict(color='orange', width=2)),
        row=3, col=1
    )
    fig.add_trace(
        go.Scatter(x=val_test_df['cycle_idx'], y=val_test_df['HI_std_ma'],
                   name='HI Volatility MA', line=dict(color='brown', width=1, dash='dash')),
        row=3, col=1
    )
    fig.add_hline(y=stable_threshold, line=dict(color='gray', dash='dot'),
                 annotation_text='Threshold', row=3, col=1)
    
    # 구간 구분선
    for row in range(1, 4):
        fig.add_vline(x=val_start, line=dict(color='gray', dash='dash', width=1),
                     annotation_text='Val', row=row, col=1)
        fig.add_vline(x=test_start, line=dict(color='gray', dash='dash', width=1),
                     annotation_text='Test', row=row, col=1)
        if first_event is not None:
            fig.add_vline(x=first_event, line=dict(color='red', dash='dashdot', width=2),
                         annotation_text='Event', row=row, col=1)
    
    fig.update_xaxes(title_text="Cycle", row=3, col=1)
    fig.update_layout(height=900, showlegend=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    