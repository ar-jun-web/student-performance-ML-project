import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import json

# ══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AcademyFlow | Student Performance ",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    """
    <div style='
        padding:40px;
        border-radius:20px;
        background: linear-gradient(135deg, #2b2d6e, #3f2b96);
        color:white;
        text-align:center;
    '>

        <h1 style='margin-bottom:10px; font-size:38px; font-weight:600;'>
            AcademyFlow
        </h1>

        <p style='opacity:0.85; font-size:16px;'>
            Advanced analytics engine for student performance prediction and personalized insights
        </p>

    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# LOAD MODEL
# ══════════════════════════════════════════════════════════════
@st.cache_resource
def load_enhanced_model():
    for path in ["enhanced_model.pkl", "model.pkl", "MLmodels/enhanced_model.pkl", "MLmodels/model.pkl"]:
        if os.path.exists(path):
            try:
                model_package = joblib.load(path)
                if isinstance(model_package, dict):
                    return model_package, True, "enhanced"
                else:
                    return {'best_model': model_package}, True, "basic"
            except:
                continue
    return None, False, None

model_package, model_loaded, model_type = load_enhanced_model()

# ══════════════════════════════════════════════════════════════
# CUSTOM CSS - MODERN GLASSMORPHISM DESIGN
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --secondary: #8b5cf6;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --glass-bg: rgba(255, 255, 255, 0.08);
    --glass-border: rgba(255, 255, 255, 0.18);
}

*:not(.material-icons):not(.material-symbols-outlined) { font-family: 'Outfit', sans-serif !important; }

/* ── Background ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
    background-attachment: fixed;
}
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: 
        radial-gradient(circle at 20% 50%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.15) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 27, 75, 0.95) 100%);
    backdrop-filter: blur(20px);
    border-right: 1px solid var(--glass-border);
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

/* ── Glass Cards ── */
.glass-card {
    background: var(--glass-bg);
    backdrop-filter: blur(16px);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 1.8rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.glass-card:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.25);
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(99, 102, 241, 0.15);
}

/* ── Hero Section ── */
.hero-container {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 24px;
    padding: 3rem 2.5rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}
.hero-container::before {
    content: '';
    position: absolute;
    top: -50%; right: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%);
    animation: rotate 20s linear infinite;
}
@keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    color: white;
    padding: 0.5rem 1.2rem;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 1rem;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}
.hero-title {
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #fff 0%, #a5b4fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.5rem 0 1rem 0;
    line-height: 1.2;
}
.hero-subtitle {
    font-size: 1.15rem;
    color: #cbd5e1;
    font-weight: 400;
    margin: 0;
}

/* ── Metric Cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
}
.metric-box {
    background: var(--glass-bg);
    backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.metric-box::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    transform: scaleX(0);
    transition: transform 0.3s ease;
}
.metric-box:hover::after { transform: scaleX(1); }
.metric-box:hover {
    background: rgba(255, 255, 255, 0.12);
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.2);
}
.metric-icon { font-size: 2.2rem; margin-bottom: 0.5rem; }
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #a5b4fc;
    margin: 0.2rem 0;
}
.metric-label {
    font-size: 0.75rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}

/* ── Section Headers ── */
.section-header {
    font-size: 1.4rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 2rem 0 1.2rem 0;
    padding-left: 1rem;
    border-left: 4px solid var(--primary);
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

/* ── Prediction Results ── */
.prediction-card {
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin: 1.5rem 0;
}
.prediction-card.excellent {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.25) 0%, rgba(5, 150, 105, 0.15) 100%);
    border: 2px solid rgba(16, 185, 129, 0.5);
}
.prediction-card.good {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.25) 0%, rgba(37, 99, 235, 0.15) 100%);
    border: 2px solid rgba(59, 130, 246, 0.5);
}
.prediction-card.average {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.25) 0%, rgba(217, 119, 6, 0.15) 100%);
    border: 2px solid rgba(245, 158, 11, 0.5);
}
.prediction-card.poor {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.25) 0%, rgba(220, 38, 38, 0.15) 100%);
    border: 2px solid rgba(239, 68, 68, 0.5);
}

.prediction-emoji { font-size: 4rem; margin-bottom: 1rem; }
.prediction-label {
    font-size: 1.8rem;
    font-weight: 800;
    color: #fff;
    margin: 0.5rem 0;
    text-transform: uppercase;
    letter-spacing: 2px;
}
.prediction-score {
    font-size: 3.5rem;
    font-weight: 900;
    color: #f1f5f9;
    margin: 0.5rem 0;
    font-family: 'JetBrains Mono', monospace !important;
}
.prediction-desc {
    font-size: 1rem;
    color: #cbd5e1;
    margin-top: 1rem;
    line-height: 1.6;
}

/* ── Model Badge ── */
.model-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(99, 102, 241, 0.2);
    border: 1px solid rgba(99, 102, 241, 0.4);
    padding: 0.6rem 1.2rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #a5b4fc;
    margin-top: 1rem;
}

/* ── Insights Cards ── */
.insight-card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 0.8rem 0;
}
.insight-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.insight-text {
    font-size: 0.95rem;
    color: #cbd5e1;
    line-height: 1.7;
}

/* ── Progress Bars ── */
.progress-container {
    background: rgba(15, 23, 42, 0.5);
    border-radius: 50px;
    height: 12px;
    overflow: hidden;
    margin: 0.8rem 0;
}
.progress-bar {
    height: 100%;
    border-radius: 50px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    width: 100%;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(99, 102, 241, 0.6) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 1rem;
    background: rgba(15, 23, 42, 0.5);
    border-radius: 12px;
    padding: 0.5rem;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
    padding: 0.8rem 1.5rem !important;
}
.stTabs [aria-selected="true"] {
    background: var(--primary) !important;
    color: white !important;
}

/* ── Animations ── */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
.animate-in {
    animation: fadeInUp 0.6s ease-out;
}

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Hide Sidebar Collapse Button ── */
[data-testid="collapsedControl"] { display: none !important; }
button[kind="header"] { display: none !important; }
[data-testid="stSidebarCollapseButton"] { display: none !important; }
section[data-testid="stSidebar"] > div:first-child > div:first-child button { display: none !important; }
.st-emotion-cache-1dp5vir { display: none !important; }
div[data-testid="stSidebarNav"] + div button { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════

def calculate_engineered_features(hours, prev_score, extra, sleep, papers):
    """Calculate advanced features"""
    return {
        'Study_Sleep_Ratio': hours / (sleep + 1),
        'Total_Effort': hours + papers,
        'Previous_Score_Normalized': prev_score / 100,
        'Sleep_Efficiency': sleep * prev_score / 100
    }

def make_gauge_chart(value, title, max_val, color_scheme="blue"):
    """Create modern gauge chart"""
    colors = {
        "blue": ["#3b82f6", "#1d4ed8"],
        "purple": ["#8b5cf6", "#6d28d9"],
        "green": ["#10b981", "#059669"],
        "orange": ["#f59e0b", "#d97706"]
    }
    color = colors.get(color_scheme, colors["blue"])
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={'font': {'size': 32, 'color': '#f1f5f9', 'family': 'JetBrains Mono'}},
        title={'text': title, 'font': {'size': 12, 'color': '#94a3b8'}},
        gauge={
            'axis': {'range': [0, max_val], 'tickcolor': 'rgba(255,255,255,0.2)'},
            'bar': {'color': color[0], 'thickness': 0.3},
            'bgcolor': 'rgba(0,0,0,0)',
            'borderwidth': 0,
            'steps': [
                {'range': [0, max_val*0.33], 'color': 'rgba(239,68,68,0.15)'},
                {'range': [max_val*0.33, max_val*0.66], 'color': 'rgba(245,158,11,0.15)'},
                {'range': [max_val*0.66, max_val], 'color': 'rgba(16,185,129,0.15)'}
            ],
            'threshold': {
                'line': {'color': color[1], 'width': 4},
                'thickness': 0.8,
                'value': value
            }
        }
    ))
    fig.update_layout(
        height=220,
        margin=dict(l=20, r=20, t=50, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#f1f5f9'}
    )
    return fig

def make_radar_chart(values, categories):
    """Create student profile radar"""
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(99,102,241,0.2)',
        line=dict(color='#6366f1', width=3),
        marker=dict(color='#8b5cf6', size=8)
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color='rgba(255,255,255,0.4)', size=9),
                gridcolor='rgba(255,255,255,0.1)'
            ),
            angularaxis=dict(
                tickfont=dict(color='#cbd5e1', size=11),
                gridcolor='rgba(255,255,255,0.1)'
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        height=350,
        margin=dict(l=80, r=80, t=30, b=30)
    )
    return fig

def make_comparison_chart(student_scores, avg_scores, categories):
    """Create student vs average comparison"""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Your Score',
        x=categories,
        y=student_scores,
        marker_color='#6366f1',
        text=[f'{v}%' for v in student_scores],
        textposition='outside'
    ))
    fig.add_trace(go.Bar(
        name='Class Average',
        x=categories,
        y=avg_scores,
        marker_color='#8b5cf6',
        opacity=0.6
    ))
    fig.update_layout(
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#cbd5e1'),
        height=320,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.08)', title='Score %'),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )
    return fig

# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:1.5rem 0 1rem 0;'>
        <div style='font-size:2.5rem; margin-bottom:0.5rem;'>🎯</div>
        <<div style='font-size:1.5rem; font-weight:800; color:#a5b4fc; margin-bottom:0.3rem;'>AcademyFlow</div>
        <div style='font-size:0.85rem; color:#64748b; font-weight:500;'>Student Performance Analysis</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 Student Inputs")
    
    hours_studied = st.slider("📚 Hours Studied / Day", 0, 12, 6, help="Daily study hours")
    previous_scores = st.slider("📈 Previous Scores (%)", 0, 100, 75, help="Last exam score")
    extracurricular = st.selectbox("🏆 Extracurricular Activities", ["Yes", "No"])
    sleep_hours = st.slider("😴 Sleep Hours / Night", 4, 12, 7, help="Average nightly sleep")
    sample_papers = st.slider("📝 Practice Papers Done", 0, 10, 4, help="Mock tests completed")
    
    st.markdown("---")
    
    # Goal setting
    st.markdown("### 🎯 Set Your Goal")
    target_score = st.slider("Target Performance Index", 50, 100, 85)
    
    st.markdown("---")
    
    predict_btn = st.button("🔮 Predict Performance", use_container_width=True)
    
    st.markdown("---")
    
    # Model info
    if model_loaded:
        model_name = model_package.get('best_model_name', 'Linear Regression')
        st.markdown(f"""
        <div style='background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.3);
                    border-radius:12px; padding:1rem; text-align:center;'>
            <div style='font-size:0.75rem; color:#6ee7b7; margin-bottom:0.3rem;'>✓ MODEL LOADED</div>
            <div style='font-size:0.9rem; font-weight:700; color:#d1fae5;'>{model_name}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("⚠️ Model not found")

# ══════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════

# Hero Section
st.markdown("""
<div class='hero-container animate-in'>
    <div style='position:relative; z-index:1;'>
        <div class='hero-badge'>🚀 NEXT-GEN ANALYTICS</div>
        <h1 class='hero-title'>AcademyFlow</h1>
        <p class='hero-subtitle'>
            Advanced analytics engine for student performance prediction and personalized insights
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Metric Cards
extra_enc = 1 if extracurricular == "Yes" else 0

st.markdown("""
<div class='metric-grid'>
    <div class='metric-box'>
        <div class='metric-icon'>📚</div>
        <div class='metric-value'>{}</div>
        <div class='metric-label'>Study Hours</div>
    </div>
    <div class='metric-box'>
        <div class='metric-icon'>📊</div>
        <div class='metric-value'>{}%</div>
        <div class='metric-label'>Previous Score</div>
    </div>
    <div class='metric-box'>
        <div class='metric-icon'>🏆</div>
        <div class='metric-value'>{}</div>
        <div class='metric-label'>Extra-Curricular</div>
    </div>
    <div class='metric-box'>
        <div class='metric-icon'>😴</div>
        <div class='metric-value'>{}</div>
        <div class='metric-label'>Sleep Hours</div>
    </div>
    <div class='metric-box'>
        <div class='metric-icon'>📝</div>
        <div class='metric-value'>{}</div>
        <div class='metric-label'>Practice Papers</div>
    </div>
</div>
""".format(hours_studied, previous_scores, extracurricular, sleep_hours, sample_papers), 
unsafe_allow_html=True)

# Main Layout
tab1, tab2, tab3, tab4 = st.tabs(["📊 Performance Analysis", "🎯 Goal Tracker", "📈 Peer Comparison", "💡 Study Insights"])

with tab1:
    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        st.markdown('<div class="section-header">📊 Performance Metrics</div>', unsafe_allow_html=True)
        
        # Gauges
        g1, g2, g3 = st.columns(3)
        with g1:
            st.plotly_chart(make_gauge_chart(hours_studied, "Study Hours", 12, "blue"), use_container_width=True)
        with g2:
            st.plotly_chart(make_gauge_chart(previous_scores, "Previous Score", 100, "purple"), use_container_width=True)
        with g3:
            st.plotly_chart(make_gauge_chart(sleep_hours, "Sleep Hours", 12, "green"), use_container_width=True)
        
        # Radar Chart
        st.markdown('<div class="section-header">🕸️ Student Profile Analysis</div>', unsafe_allow_html=True)
        radar_values = [
            (hours_studied / 12) * 100,
            previous_scores,
            (sleep_hours / 12) * 100,
            (sample_papers / 10) * 100,
            100 if extracurricular == "Yes" else 20
        ]
        radar_categories = ["Study Time", "Academic Record", "Sleep Quality", "Practice", "Activities"]
        st.plotly_chart(make_radar_chart(radar_values, radar_categories), use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">🔮 Prediction</div>', unsafe_allow_html=True)
        
        if predict_btn and model_loaded:
            # Prepare features
            eng_features = calculate_engineered_features(
                hours_studied, previous_scores, extra_enc, sleep_hours, sample_papers
            )
            
            if model_type == "enhanced":
                # Use enhanced model with all features
                features_df = pd.DataFrame({
                    'Hours Studied': [hours_studied],
                    'Previous Scores': [previous_scores],
                    'Extracurricular Activities': [extra_enc],
                    'Sleep Hours': [sleep_hours],
                    'Sample Question Papers Practiced': [sample_papers],
                    'Study_Sleep_Ratio': [eng_features['Study_Sleep_Ratio']],
                    'Total_Effort': [eng_features['Total_Effort']],
                    'Previous_Score_Normalized': [eng_features['Previous_Score_Normalized']],
                    'Sleep_Efficiency': [eng_features['Sleep_Efficiency']]
                })
                model = model_package['best_model']
                model_name = model_package.get('best_model_name', 'Unknown')
            else:
                # Basic model
                features_df = np.array([[hours_studied, previous_scores, extra_enc, sleep_hours, sample_papers]])
                model = model_package['best_model']
                model_name = "Linear Regression"
            
            # Predict
            prediction = float(model.predict(features_df)[0])
            prediction = np.clip(prediction, 0, 100)
            
            # Determine grade
            if prediction >= 85:
                grade_class, emoji, status, message = "excellent", "🏆", "EXCELLENT", "Outstanding performance! Keep up the excellent work!"
            elif prediction >= 70:
                grade_class, emoji, status, message = "good", "⭐", "GOOD", "Strong performance with room to reach excellence!"
            elif prediction >= 50:
                grade_class, emoji, status, message = "average", "📈", "AVERAGE", "Decent performance. Increase efforts to improve further."
            else:
                grade_class, emoji, status, message = "poor", "⚠️", "NEEDS IMPROVEMENT", "Focus on fundamentals and increase study time."
            
            st.markdown(f"""
            <div class='prediction-card {grade_class}'>
                <div class='prediction-emoji'>{emoji}</div>
                <div class='prediction-label'>{status}</div>
                <div class='prediction-score'>{prediction:.1f}</div>
                <div class='prediction-desc'>{message}</div>
                <div class='model-badge'>
                    <span>Powered by {model_name}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Gap analysis
            gap = target_score - prediction
            if gap > 0:
                st.markdown(f"""
                <div class='glass-card' style='margin-top:1.5rem; text-align:center;'>
                    <div style='font-size:1.1rem; font-weight:700; color:#f59e0b; margin-bottom:1rem;'>
                        📊 Goal Gap Analysis
                    </div>
                    <div style='font-size:2.5rem; font-weight:800; color:#fbbf24; margin:0.5rem 0;'>
                        {gap:.1f}
                    </div>
                    <div style='color:#cbd5e1; font-size:0.95rem;'>
                        points needed to reach your target of {target_score}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='glass-card' style='text-align:center; padding:3rem 2rem;'>
                <div style='font-size:3rem; margin-bottom:1rem;'>🎯</div>
                <div style='font-size:1.2rem; color:#cbd5e1; line-height:1.8;'>
                    Adjust the parameters in the sidebar,<br>
                    then click <strong style='color:#a5b4fc;'>Predict Performance</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-header">🎯 Goal Progress Tracker</div>', unsafe_allow_html=True)
    
    if predict_btn and model_loaded:
        current_score = prediction
        progress_pct = min((current_score / target_score) * 100, 100)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class='glass-card'>
                <div style='font-size:0.9rem; color:#94a3b8; margin-bottom:0.5rem;'>CURRENT PERFORMANCE</div>
                <div style='font-size:3rem; font-weight:800; color:#6366f1;'>{current_score:.1f}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='glass-card'>
                <div style='font-size:0.9rem; color:#94a3b8; margin-bottom:0.5rem;'>TARGET SCORE</div>
                <div style='font-size:3rem; font-weight:800; color:#8b5cf6;'>{target_score}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='glass-card' style='margin-top:1.5rem;'>
            <div style='display:flex; justify-content:space-between; margin-bottom:1rem;'>
                <span style='font-weight:700; color:#f1f5f9;'>Progress to Goal</span>
                <span style='font-weight:700; color:#a5b4fc;'>{progress_pct:.1f}%</span>
            </div>
            <div class='progress-container'>
                <div class='progress-bar' style='width:{progress_pct}%;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Recommendations to reach goal
        if current_score < target_score:
            st.markdown('<div class="section-header">💡 Recommended Actions</div>', unsafe_allow_html=True)
            
            recommendations = []
            if hours_studied < 8:
                recommendations.append(("📚", "Increase Study Time", f"Try studying {min(hours_studied + 2, 10)} hours/day to boost performance"))
            if sample_papers < 7:
                recommendations.append(("📝", "Practice More Papers", f"Complete {min(sample_papers + 3, 10)} practice papers for better preparation"))
            if sleep_hours < 7:
                recommendations.append(("😴", "Improve Sleep", "Aim for 7-8 hours of sleep for better memory retention"))
            if extracurricular == "No":
                recommendations.append(("🏆", "Join Activities", "Extracurricular activities correlate with better performance"))
            
            for icon, title, desc in recommendations[:3]:
                st.markdown(f"""
                <div class='insight-card'>
                    <div class='insight-title'>{icon} {title}</div>
                    <div class='insight-text'>{desc}</div>
                </div>
                """, unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-header">📈 Peer Comparison</div>', unsafe_allow_html=True)
    
    # Simulated class averages
    avg_scores = [60, 70, 65, 60, 50]  # Average for: study, prev, sleep, papers, extra
    student_scores = [
        (hours_studied / 12) * 100,
        previous_scores,
        (sleep_hours / 12) * 100,
        (sample_papers / 10) * 100,
        100 if extra_enc else 20
    ]
    categories = ["Study Time", "Academic", "Sleep", "Practice", "Activities"]
    
    st.plotly_chart(make_comparison_chart(student_scores, avg_scores, categories), use_container_width=True)
    
    # Strengths and weaknesses
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">💪 Your Strengths</div>', unsafe_allow_html=True)
        strengths = []
        for i, (s, a, cat) in enumerate(zip(student_scores, avg_scores, categories)):
            if s > a + 10:
                strengths.append((cat, s, a))
        
        if strengths:
            for cat, s, a in strengths[:3]:
                st.markdown(f"""
                <div class='glass-card' style='border-left:3px solid #10b981;'>
                    <div style='font-weight:700; color:#10b981; margin-bottom:0.3rem;'>✓ {cat}</div>
                    <div style='color:#cbd5e1; font-size:0.9rem;'>
                        You're {s-a:.0f}% above class average
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Keep working to build your strengths!")
    
    with col2:
        st.markdown('<div class="section-header">🎯 Areas to Improve</div>', unsafe_allow_html=True)
        weaknesses = []
        for i, (s, a, cat) in enumerate(zip(student_scores, avg_scores, categories)):
            if s < a - 5:
                weaknesses.append((cat, s, a))
        
        if weaknesses:
            for cat, s, a in weaknesses[:3]:
                st.markdown(f"""
                <div class='glass-card' style='border-left:3px solid #f59e0b;'>
                    <div style='font-weight:700; color:#f59e0b; margin-bottom:0.3rem;'>! {cat}</div>
                    <div style='color:#cbd5e1; font-size:0.9rem;'>
                        Focus area - {a-s:.0f}% below average
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("Great! You're performing well across all areas!")

with tab4:
    st.markdown('<div class="section-header">💡 Personalized Study Insights</div>', unsafe_allow_html=True)
    
    insights = []
    
    # Study time insights
    if hours_studied >= 8:
        insights.append(("📚", "Excellent Study Commitment", 
                        f"Your {hours_studied} hours of daily study is exceptional. Maintain this consistency!", 
                        "success"))
    elif hours_studied >= 5:
        insights.append(("📖", "Good Study Routine", 
                        f"{hours_studied} hours is solid, but pushing to 7-8 hours can significantly boost results.", 
                        "info"))
    else:
        insights.append(("⏰", "Increase Study Time", 
                        f"Only {hours_studied} hours/day may not be enough. Try gradually increasing to 6-7 hours.", 
                        "warning"))
    
    # Sleep insights
    if 7 <= sleep_hours <= 9:
        insights.append(("😴", "Optimal Sleep Schedule", 
                        f"{sleep_hours} hours of sleep is perfect for memory consolidation and cognitive function.", 
                        "success"))
    elif sleep_hours < 7:
        insights.append(("🌙", "Sleep More", 
                        f"{sleep_hours} hours may not be enough. Aim for 7-8 hours to improve retention and focus.", 
                        "warning"))
    else:
        insights.append(("⏰", "Too Much Sleep?", 
                        f"{sleep_hours} hours might be excessive. 7-8 hours is optimal for most students.", 
                        "info"))
    
    # Practice insights
    if sample_papers >= 7:
        insights.append(("📝", "Excellent Exam Prep", 
                        f"{sample_papers} practice papers shows strong preparation. This is a top predictor of success!", 
                        "success"))
    elif sample_papers >= 4:
        insights.append(("📋", "Good Practice Routine", 
                        f"{sample_papers} papers is decent. Push to 7-8 for maximum exam confidence.", 
                        "info"))
    else:
        insights.append(("📄", "Practice More", 
                        f"Only {sample_papers} papers practiced. This is crucial - aim for at least 6-7 before exams.", 
                        "warning"))
    
    # Extracurricular insights
    if extracurricular == "Yes":
        insights.append(("🏆", "Well-Rounded Profile", 
                        "Extracurricular participation builds discipline and correlates with higher academic performance.", 
                        "success"))
    else:
        insights.append(("🎯", "Consider Activities", 
                        "Joining clubs or sports can improve time management and overall academic outcomes.", 
                        "info"))
    
    # Previous scores insight
    if previous_scores >= 85:
        insights.append(("⭐", "Strong Academic Foundation", 
                        f"{previous_scores}% shows excellent prior knowledge. Build on this momentum!", 
                        "success"))
    elif previous_scores >= 70:
        insights.append(("📊", "Solid Performance", 
                        f"{previous_scores}% is good. Focus on weak topics to push into the 85+ range.", 
                        "info"))
    else:
        insights.append(("📉", "Foundation Building Needed", 
                        f"{previous_scores}% suggests knowledge gaps. Consider focused revision on core topics.", 
                        "warning"))
    
    # Display insights
    for icon, title, desc, level in insights:
        color_map = {
            "success": ("#10b981", "rgba(16,185,129,0.15)"),
            "info": ("#3b82f6", "rgba(59,130,246,0.15)"),
            "warning": ("#f59e0b", "rgba(245,158,11,0.15)")
        }
        border_color, bg_color = color_map[level]
        
        st.markdown(f"""
        <div class='insight-card' style='background:{bg_color}; border-left:3px solid {border_color};'>
            <div class='insight-title' style='color:{border_color};'>{icon} {title}</div>
            <div class='insight-text'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align:center; color:#475569; font-size:0.85rem; 
            padding:2rem 0 1rem; margin-top:3rem;
            border-top:1px solid rgba(255,255,255,0.08);'>
    <div style='margin-bottom:0.5rem;'>🎓 AcademyFlow - Advanced Student Performance Analytics</div>
    <div>Built with Streamlit</div>
</div>
""", unsafe_allow_html=True)
