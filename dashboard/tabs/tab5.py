import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.dataloader_local import load_correlation_data

def render(battery_id, model_type, preprocessing):
    st.subheader("Correlation Analysis")
    
    # 데이터 로드
    df_merged, metadata = load_correlation_data(battery_id, model_type, preprocessing)
    
    # 메타데이터 추출
    pearson_cap = metadata['pearson_cap']
    p_p_cap = metadata['p_p_cap']
    pearson_rohm = metadata['pearson_rohm']
    p_p_rohm = metadata['p_p_rohm']
    
    # 2x2 서브플롯 생성
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            f'Anomaly Score vs Capacity<br>Pearson r={pearson_cap:.3f}',
            f'Anomaly Score vs R_ohmic<br>Pearson r={pearson_rohm:.3f}',
            'Anomaly Score & Capacity Over Cycles',
            'Anomaly Score & R_ohmic Over Cycles'
        ),
        specs=[
            [{"type": "scatter"}, {"type": "scatter"}],
            [{"secondary_y": True}, {"secondary_y": True}]
        ],
        vertical_spacing=0.20,
        horizontal_spacing=0.15
    )
    
    # 1) Scatter: Anomaly Score vs Capacity
    fig.add_trace(
        go.Scatter(
            x=df_merged['mean_score'], 
            y=df_merged['Capacity'],
            mode='markers',
            marker=dict(size=8, color='blue', opacity=0.6, line=dict(color='black', width=0.5)),
            name='Data',
            showlegend=False
        ),
        row=1, col=1
    )
    
    # 회귀선
    z1 = np.polyfit(df_merged['mean_score'], df_merged['Capacity'], 1)
    p1 = np.poly1d(z1)
    x_line1 = np.linspace(df_merged['mean_score'].min(), df_merged['mean_score'].max(), 100)
    fig.add_trace(
        go.Scatter(
            x=x_line1, 
            y=p1(x_line1),
            mode='lines',
            line=dict(color='red', dash='dash', width=2),
            name='Regression',
            showlegend=False
        ),
        row=1, col=1
    )
    
    # 2) Scatter: Anomaly Score vs R_ohmic
    fig.add_trace(
        go.Scatter(
            x=df_merged['mean_score'], 
            y=df_merged['R_ohmic'],
            mode='markers',
            marker=dict(size=8, color='green', opacity=0.6, line=dict(color='black', width=0.5)),
            name='Data',
            showlegend=False
        ),
        row=1, col=2
    )
    
    # 회귀선
    z2 = np.polyfit(df_merged['mean_score'], df_merged['R_ohmic'], 1)
    p2 = np.poly1d(z2)
    fig.add_trace(
        go.Scatter(
            x=x_line1, 
            y=p2(x_line1),
            mode='lines',
            line=dict(color='red', dash='dash', width=2),
            name='Regression',
            showlegend=False
        ),
        row=1, col=2
    )
    
    # 3) Time series: Anomaly Score & Capacity
    fig.add_trace(
        go.Scatter(
            x=df_merged['cycle'], 
            y=df_merged['mean_score'],
            mode='lines+markers',
            line=dict(color='blue', width=2),
            marker=dict(size=4),
            name='Anomaly Score'
        ),
        row=2, col=1, secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=df_merged['cycle'], 
            y=df_merged['Capacity'],
            mode='lines+markers',
            line=dict(color='red', width=2),
            marker=dict(size=4, symbol='square'),
            name='Capacity'
        ),
        row=2, col=1, secondary_y=True
    )
    
    # 4) Time series: Anomaly Score & R_ohmic
    fig.add_trace(
        go.Scatter(
            x=df_merged['cycle'], 
            y=df_merged['mean_score'],
            mode='lines+markers',
            line=dict(color='blue', width=2),
            marker=dict(size=4),
            name='Anomaly Score',
            showlegend=False
        ),
        row=2, col=2, secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=df_merged['cycle'], 
            y=df_merged['R_ohmic'],
            mode='lines+markers',
            line=dict(color='green', width=2),
            marker=dict(size=4, symbol='square'),
            name='R_ohmic'
        ),
        row=2, col=2, secondary_y=True
    )
    
    # 축 레이블
    fig.update_xaxes(title_text="Anomaly Score", row=1, col=1)
    fig.update_xaxes(title_text="Anomaly Score", row=1, col=2)
    fig.update_xaxes(title_text="Cycle", row=2, col=1)
    fig.update_xaxes(title_text="Cycle", row=2, col=2)
    
    fig.update_yaxes(title_text="Capacity (Ah)", row=1, col=1)
    fig.update_yaxes(title_text="R_ohmic (Ω)", row=1, col=2)
    fig.update_yaxes(title_text="Anomaly Score", secondary_y=False, row=2, col=1)
    fig.update_yaxes(title_text="Capacity (Ah)", secondary_y=True, row=2, col=1)
    fig.update_yaxes(title_text="Anomaly Score", secondary_y=False, row=2, col=2)
    fig.update_yaxes(title_text="R_ohmic (Ω)", secondary_y=True, row=2, col=2)

    fig.update_layout(
        height=1000,
        showlegend=False,
        hovermode='x unified',
    )
    
    st.plotly_chart(fig, use_container_width=True)