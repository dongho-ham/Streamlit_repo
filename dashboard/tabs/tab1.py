import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.dataloader import load_discharge_summary


def render(battery_id):
    discharge_summary = load_discharge_summary(battery_id)
    
    st.subheader(f"{battery_id} Battery Overview")
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Capacity', 'Min Voltage', 'Max Temp', 'Discharge Time'),
        vertical_spacing=0.20,
        horizontal_spacing=0.15
    )
    
    # 용량
    fig.add_trace(
        go.Scatter(x=discharge_summary['cycle_idx'], y=discharge_summary['capacity'],
                   mode='lines+markers', name='Capacity',
                   line=dict(color='blue', width=2), marker=dict(size=4)),
        row=1, col=1
    )
    
    # 방전 전압
    fig.add_trace(
        go.Scatter(x=discharge_summary['cycle_idx'], y=discharge_summary['dis_volt_min'],
                   mode='lines+markers', name='Min Voltage',
                   line=dict(color='green', width=2), marker=dict(size=4)),
        row=1, col=2
    )
    
    # 온도
    fig.add_trace(
        go.Scatter(x=discharge_summary['cycle_idx'], y=discharge_summary['dis_temp_max'],
                   mode='lines+markers', name='Max Temp',
                   line=dict(color='red', width=2), marker=dict(size=4)),
        row=2, col=1
    )
    
    # 방전 시간
    fig.add_trace(
        go.Scatter(x=discharge_summary['cycle_idx'], y=discharge_summary['dis_time'],
                   mode='lines+markers', name='Discharge Time',
                   line=dict(color='orange', width=2), marker=dict(size=4)),
        row=2, col=2
    )
    
    # 축 레이블
    fig.update_xaxes(title_text="cycle", row=1, col=1)
    fig.update_xaxes(title_text="cycle", row=1, col=2)
    fig.update_xaxes(title_text="cycle", row=2, col=1)
    fig.update_xaxes(title_text="cycle", row=2, col=2)

    fig.update_yaxes(title_text="Capacity (Ah)", row=1, col=1)
    fig.update_yaxes(title_text="Voltage (V)", row=1, col=2)
    fig.update_yaxes(title_text="Temperature (℃)", row=2, col=1)
    fig.update_yaxes(title_text="Time (sec)", row=2, col=2)

    fig.update_layout(
        height=700,
        showlegend=False,
        hovermode='x unified',
        title_text="Cycle-by-Cycle Battery Discharge Data Summary",
        title_font_size=20
    )
    
    st.plotly_chart(fig, use_container_width=True)