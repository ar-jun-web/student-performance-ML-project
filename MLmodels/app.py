import streamlit as st
import numpy as np
import pickle
import os
import plotly.graph_objects as go

st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: #e0e0e0;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    border-right: 1px solid rgba(100,149,237,0.3);
}
.hero-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2.5rem 2rem; border-radius: 20px; text-align: center;
    margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(102,126,234,0.4);
}
.hero-title  { font-size: 2.8rem; font-weight: 800; color: white; margin: 0; }
.hero-subtitle { font-size: 1.1rem; color: rgba(255,255,255,0.85); margin-top: 0.5rem; }
.metric-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
    border: 1px solid rgba(255,255,255,0.12); border-radius: 16px;
    padding: 1.4rem 1.2rem; text-align: center;
}
.metric-icon  { font-size: 2rem; }
.metric-value { font-size: 1.9rem; font-weight: 700; color: #a78bfa; margin: .3rem 0 0; }
.metric-label { font-size: .8rem; color: rgba(255,255,255,0.55); text-transform: uppercase; letter-spacing: 1px; }
.result-box { border-radius: 20px; padding: 2rem; text-align: center; margin: 1.5rem 0; font-weight: 600; }
.result-pass { background: linear-gradient(135deg,#11998e,#38ef7d); color:#fff; box-shadow:0 8px 25px rgba(56,239,125,.35); }
.result-fail { background: linear-gradient(135deg,#eb3349,#f45c43); color:#fff; box-shadow:0 8px 25px rgba(235,51,73,.35); }
.result-avg  { background: linear-gradient(135deg,#f7971e,#ffd200); color:#1a1a1a; box-shadow:0 8px 25px rgba(255,210,0,.35); }
.section-header {
    font-size: 1.3rem; font-weight: 700; color: #a78bfa;
    border-left: 4px solid #667eea; padding-left: .75rem; margin: 1.5rem 0 1rem;
}
.stButton > button {
    background: linear-gradient(135deg,#667eea,#764ba2) !important;
    color: white !important; border: none !important; border-radius: 12px !important;
    padding: .75rem 2.5rem !important; font-size: 1.05rem !important;
    font-weight: 700 !important; width: 100%;
    box-shadow: 0 4px 18px rgba(102,126,234,.45) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Load model ──────────────────────────────
@st.cache_resource
def load_model():
    for path in ["model.pkl", "MLmodels/model.pkl"]:
        if os.path.exists(path):
            with open(path, "rb") as f:
                return pickle.load(f), True
    return None, False

model, model_loaded = load_model()


# ── Charts ──────────────────────────────────
def make_gauge(score, title, max_val=100):
    pct = (score / max_val) * 100
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=score,
        number={"font": {"size": 28, "color": "#a78bfa"}},
        title={"text": title, "font": {"size": 13, "color": "rgba(255,255,255,0.7)"}},
        gauge={
            "axis": {"range": [0, max_val], "tickcolor": "rgba(255,255,255,0.3)"},
            "bar":  {"color": "#667eea", "thickness": 0.25},
            "bgcolor": "rgba(0,0,0,0)",
            "steps": [
                {"range": [0,   max_val*0.4], "color": "rgba(235,51,73,0.25)"},
                {"range": [max_val*0.4, max_val*0.7], "color": "rgba(255,210,0,0.20)"},
                {"range": [max_val*0.7, max_val],     "color": "rgba(56,239,125,0.20)"},
            ],
            "threshold": {"line": {"color": "#a78bfa", "width": 3},
                          "thickness": 0.75, "value": score},
        },
    ))
    fig.update_layout(height=200, margin=dict(l=15,r=15,t=40,b=5),
                      paper_bgcolor="rgba(0,0,0,0)", font={"color":"white"})
    return fig


def make_bar(labels, values, colors):
    fig = go.Figure(go.Bar(
        x=labels, y=values, marker=dict(color=colors),
        text=[str(v) for v in values], textposition="outside",
        textfont=dict(color="white", size=12),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(tickfont=dict(size=10), gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
        height=280, margin=dict(l=5,r=5,t=20,b=5), bargap=0.4,
    )
    return fig


def make_radar(values, categories):
    fig = go.Figure(go.Scatterpolar(
        r=values + [values[0]], theta=categories + [categories[0]],
        fill="toself", fillcolor="rgba(102,126,234,0.25)",
        line=dict(color="#a78bfa", width=2.5),
        marker=dict(color="#667eea", size=7),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0,100],
                            tickfont=dict(color="rgba(255,255,255,0.4)", size=8),
                            gridcolor="rgba(255,255,255,0.1)"),
            angularaxis=dict(tickfont=dict(color="rgba(255,255,255,0.8)", size=11),
                             gridcolor="rgba(255,255,255,0.1)"),
        ),
        paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
        height=300, margin=dict(l=40,r=40,t=20,b=20),
    )
    return fig


# ── SIDEBAR ─────────────────────────────────
with st.sidebar:
    st.markdown('<div style="font-size:1.4rem;text-align:center;color:#a78bfa;font-weight:800;padding:.5rem 0;">🎓 Enter Student Details</div>', unsafe_allow_html=True)
    st.markdown("---")

    hours_studied    = st.slider("📖 Hours Studied",                  0, 12, 6)
    previous_scores  = st.slider("📊 Previous Scores",                0, 100, 65)
    extracurricular  = st.selectbox("🏅 Extracurricular Activities",  ["Yes", "No"])
    sleep_hours      = st.slider("😴 Sleep Hours",                    4, 12, 7)
    sample_papers    = st.slider("📝 Sample Question Papers Practiced", 0, 10, 3)

    st.markdown("---")
    predict_btn = st.button("🔮  Predict Performance")


# ── HERO ────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🎓 Student Performance Predictor</div>
    <div class="hero-subtitle">AI-powered academic performance analysis · Final Year ML Project</div>
</div>""", unsafe_allow_html=True)


# ── TOP METRIC CARDS ────────────────────────
extra_enc    = 1 if extracurricular == "Yes" else 0
study_score  = round((hours_studied / 12) * 100)
sleep_score  = round((sleep_hours   / 12) * 100)
paper_score  = round((sample_papers / 10) * 100)

c1, c2, c3, c4, c5 = st.columns(5)
for col, icon, val, label in [
    (c1, "📖", f"{hours_studied}h",    "Hours Studied"),
    (c2, "📊", f"{previous_scores}%",  "Previous Score"),
    (c3, "🏅", extracurricular,        "Extracurricular"),
    (c4, "😴", f"{sleep_hours}h",      "Sleep Hours"),
    (c5, "📝", sample_papers,          "Papers Practiced"),
]:
    with col:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── MAIN LAYOUT ─────────────────────────────
left_col, right_col = st.columns([1.1, 1], gap="large")

with left_col:
    st.markdown('<div class="section-header">📈 Performance Gauges</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1:
        st.plotly_chart(make_gauge(hours_studied, "Hours Studied", 12), use_container_width=True)
    with g2:
        st.plotly_chart(make_gauge(previous_scores, "Previous Score", 100), use_container_width=True)
    with g3:
        st.plotly_chart(make_gauge(sleep_hours, "Sleep Hours", 12), use_container_width=True)

    st.markdown('<div class="section-header">🕸️ Student Profile Radar</div>', unsafe_allow_html=True)
    radar_vals = [study_score, previous_scores, sleep_score, paper_score,
                  100 if extracurricular == "Yes" else 20]
    radar_cats = ["Study Time", "Prev Score", "Sleep", "Practice Papers", "Extracurricular"]
    st.plotly_chart(make_radar(radar_vals, radar_cats), use_container_width=True)

with right_col:
    st.markdown('<div class="section-header">📊 Input Feature Breakdown</div>', unsafe_allow_html=True)
    bar_labels = ["Study\nHours", "Prev\nScore", "Sleep\nHours", "Papers\nPracticed", "Extra\nCurric"]
    bar_values = [hours_studied, previous_scores, sleep_hours, sample_papers, extra_enc * 10]
    bar_colors = ["#667eea", "#a78bfa", "#38ef7d", "#ffd200", "#f45c43"]
    st.plotly_chart(make_bar(bar_labels, bar_values, bar_colors), use_container_width=True)

    # ── PREDICTION ──────────────────────────
    st.markdown('<div class="section-header">🔮 Prediction Result</div>', unsafe_allow_html=True)

    if predict_btn:
        if not model_loaded:
            st.error("❌ model.pkl not found! Please save your model first.")
        else:
            features = np.array([[
                hours_studied,
                previous_scores,
                extra_enc,
                sleep_hours,
                sample_papers
            ]])

            with st.spinner("Analyzing…"):
                import time; time.sleep(0.5)
                prediction = model.predict(features)[0]
                try:
                    conf = round(max(model.predict_proba(features)[0]) * 100, 1)
                    conf_text = f"Confidence: {conf}%"
                except:
                    conf_text = f"Predicted Score: {round(float(prediction), 1)}"

            # Determine grade band
            try:
                score = float(prediction)
                if score >= 70:
                    box_class, emoji, status = "result-pass", "🏆", "HIGH PERFORMANCE"
                    tip = "Outstanding! You're on track for excellent results!"
                elif score >= 50:
                    box_class, emoji, status = "result-avg", "📈", "AVERAGE PERFORMANCE"
                    tip = "Good effort! Study more consistently to reach the top."
                else:
                    box_class, emoji, status = "result-fail", "⚠️", "NEEDS IMPROVEMENT"
                    tip = "Increase study hours, practice more papers & sleep well."
            except:
                pred_str = str(prediction).lower()
                if pred_str in ["high", "pass", "1", "good"]:
                    box_class, emoji, status = "result-pass", "🏆", "HIGH PERFORMANCE"
                    tip = "Outstanding! You're on track for excellent results!"
                elif pred_str in ["low", "fail", "0", "poor"]:
                    box_class, emoji, status = "result-fail", "⚠️", "NEEDS IMPROVEMENT"
                    tip = "Increase study hours, practice more papers & sleep well."
                else:
                    box_class, emoji, status = "result-avg", "📈", "AVERAGE PERFORMANCE"
                    tip = "Good effort! Study more consistently to reach the top."

            st.markdown(f"""<div class="result-box {box_class}">
                <div style="font-size:2.5rem;">{emoji}</div>
                <div style="font-size:1.5rem;font-weight:800;margin:.3rem 0;">{status}</div>
                <div style="font-size:1rem;opacity:.9;">{conf_text}</div>
                <div style="font-size:.9rem;margin-top:.6rem;opacity:.85;font-weight:400;">{tip}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.05);border:1px dashed rgba(167,139,250,0.4);
                    border-radius:16px;padding:2.5rem;text-align:center;color:rgba(255,255,255,0.5);">
            <div style="font-size:2.5rem;">🎯</div>
            <div style="margin-top:.5rem;">Adjust the sliders in the sidebar<br>then click <b>Predict Performance</b></div>
        </div>""", unsafe_allow_html=True)


# ── INSIGHTS ────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">💡 Smart Insights</div>', unsafe_allow_html=True)

i1, i2, i3 = st.columns(3)
for col, title, value, bg, desc in [
    (i1, "📖 Study Efficiency",
     "Strong" if hours_studied >= 7 else "Moderate" if hours_studied >= 4 else "Low",
     "rgba(102,126,234,0.15)",
     "Students studying 7+ hours/day score significantly higher on performance metrics."),
    (i2, "😴 Sleep Quality",
     "Optimal" if 7 <= sleep_hours <= 9 else "Needs Adjustment",
     "rgba(56,239,125,0.12)" if 7 <= sleep_hours <= 9 else "rgba(235,51,73,0.12)",
     "7–9 hours of sleep is optimal for memory retention and exam performance."),
    (i3, "📝 Exam Readiness",
     f"{sample_papers} Papers" ,
     "rgba(255,210,0,0.12)",
     "Practicing sample papers is one of the strongest predictors of exam success."),
]:
    with col:
        st.markdown(f"""<div style="background:{bg};border:1px solid rgba(255,255,255,0.1);
                    border-radius:16px;padding:1.2rem;">
            <div style="font-size:1rem;font-weight:700;color:#a78bfa;">{title}</div>
            <div style="font-size:1.7rem;font-weight:800;color:white;margin:.3rem 0;">{value}</div>
            <div style="font-size:.82rem;color:rgba(255,255,255,0.55);line-height:1.5;">{desc}</div>
        </div>""", unsafe_allow_html=True)


# ── FOOTER ──────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:rgba(255,255,255,0.25);font-size:.8rem;
            padding:1rem 0;border-top:1px solid rgba(255,255,255,0.07);">
    🎓 Student Performance Predictor · Final Year ML Project · Built with Streamlit
</div>""", unsafe_allow_html=True)