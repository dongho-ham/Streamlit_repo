import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.dataloader import load_anomaly_results, load_lof_cycle_summary

def get_risk_level(score, threshold):
    """위험도 분류"""
    if score > threshold * 1.5:
        return "🔴 Critical", "red"
    elif score > threshold:
        return "🟡 Warning", "orange"
    else:
        return "🟢 Normal", "green"

def render_top5_section(top_5, threshold, key_prefix):
    """Top 5 Anomalous Cycles 공통 렌더링"""
    st.markdown("---")
    st.subheader("Top 5 Anomalous Cycles")
    
    col2, col3 = st.columns([1, 2])
    
    with col2:
        st.markdown("### Cycle Rankings")
        
        for idx, (cycle, score) in enumerate(top_5, 1):
            col_a, col_b, col_c = st.columns([2, 1.2, 0.8])
            
            with col_c:
                is_checked = st.checkbox("", key=f"{key_prefix}_{int(cycle)}", label_visibility="collapsed")
            
            if is_checked:
                risk_label, risk_color = "🔵 Completed", "blue"
            else:
                risk_label, risk_color = get_risk_level(score, threshold)
            
            with col_a:
                st.markdown(f"<div style='padding-top: 8px;'><strong>{idx}. Cycle {int(cycle)}</strong></div>", 
                          unsafe_allow_html=True)
            with col_b:
                st.markdown(f"<div style='padding-top: 8px;'><span style='color:{risk_color};'>{risk_label}</span></div>", 
                          unsafe_allow_html=True)
            
            if idx < 5:
                st.markdown("<hr style='margin: 8px 0; opacity: 0.3;'>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("### Anomaly Scores (Horizontal)")
        
        fig_bar = go.Figure()
        
        colors = ['darkred' if s > threshold * 1.5 else 'orange' if s > threshold else 'gray' 
                 for _, s in top_5[::-1]]
        
        fig_bar.add_trace(go.Bar(
            y=[f"Cycle {int(c)}" for c, _ in top_5][::-1],
            x=[s for _, s in top_5][::-1],
            orientation='h',
            marker=dict(color=colors),
            text=[f"{s:.4f}" for _, s in top_5][::-1],
            textposition='outside'
        ))
        
        fig_bar.add_vline(x=threshold, line_dash="dash", line_color="red",
                         annotation_text="Threshold")
        
        fig_bar.update_layout(
            xaxis_title="Anomaly Score",
            yaxis_title="",
            height=500,
            showlegend=False,
            margin=dict(l=0, r=50, t=10, b=30)
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)

def render(battery_id, model_type, preprocessing):
    st.subheader("Anomaly Score Analysis")
    
    if model_type == "LOF":
        cycle_summary, threshold = load_lof_cycle_summary(battery_id, preprocessing)
        
        # 전체 그래프
        fig = px.scatter(cycle_summary, x='cycle_idx', y='mean_score', 
                        color='split', symbol='has_anom',
                        title='Cycle-wise LOF Anomaly (mean score per cycle)')
        fig.add_hline(y=threshold, line_dash='dash', line_color='red')
        fig.add_annotation(x=0.95, xref='paper', y=threshold,
                          text=f'Threshold: {threshold:.4f}',
                          showarrow=False, bgcolor='rgba(255,255,255,0.8)')
        st.plotly_chart(fig, use_container_width=True)
        
        # Top 5 추출
        top_5 = cycle_summary.nlargest(5, 'mean_score')[['cycle_idx', 'mean_score']].values.tolist()
        render_top5_section(top_5, threshold, "lof_check")
        return
    
    # Anomaly Transformer
    results = load_anomaly_results(battery_id, model_type, preprocessing)
    cycle_scores = results['cycle_scores']
    threshold = results['threshold']
    
    cycles = sorted(cycle_scores.keys())
    scores = [cycle_scores[c] for c in cycles]
    
    # 전체 그래프
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=cycles, y=scores, mode='lines',
                             name='Anomaly Score', line=dict(color='blue', width=2)))
    fig.add_hline(y=threshold, line_dash='dash', line_color='red')
    
    # Top 5 표시
    top_5 = sorted(cycle_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    top_cycles = [c for c, s in top_5]
    top_scores = [cycle_scores[c] for c in top_cycles]
    
    fig.add_trace(go.Scatter(x=top_cycles, y=top_scores, mode='markers+text',
                             name='Top 5 Anomalies', marker=dict(color='red', size=10),
                             text=[f'{c}' for c in top_cycles], textposition='top center'))
    
    fig.update_layout(title='Cycle-wise Anomaly Score', xaxis_title='Cycle',
                     yaxis_title='Anomaly Score', height=500, hovermode='x')
    st.plotly_chart(fig, use_container_width=True)
    
    render_top5_section(top_5, threshold, "check")