import streamlit as st
import joblib
import pandas as pd

st.set_page_config(
    page_title="ChurnSense",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #090b10 !important;
    color: #e2e8f0;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(56,189,248,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(99,102,241,0.08) 0%, transparent 55%),
        #090b10 !important;
    min-height: 100vh;
}

[data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }

/* ── Main container ── */
.block-container {
    max-width: 1100px !important;
    padding: 3rem 2rem 5rem !important;
    margin: 0 auto;
}

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3rem 0 2.5rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #38bdf8;
    margin-bottom: 0.9rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 5vw, 3.6rem);
    font-weight: 800;
    line-height: 1.05;
    background: linear-gradient(135deg, #f0f9ff 0%, #7dd3fc 45%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
}
.hero-sub {
    font-size: 1rem;
    color: #64748b;
    font-weight: 300;
    letter-spacing: 0.01em;
}
.hero-line {
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, #38bdf8, #818cf8);
    margin: 1.8rem auto 0;
    border-radius: 2px;
}

/* ── Section labels ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #475569;
    margin: 2.5rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1e293b;
}

/* ── Card panels ── */
.card {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 1.8rem 2rem;
    backdrop-filter: blur(12px);
    margin-bottom: 1.2rem;
    transition: border-color 0.25s;
}
.card:hover { border-color: rgba(56,189,248,0.15); }

/* ── Streamlit widget overrides ── */
label, .stSlider label, .stSelectbox label, .stNumberInput label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #94a3b8 !important;
    letter-spacing: 0.03em !important;
    text-transform: uppercase !important;
    margin-bottom: 4px !important;
}

/* Inputs */
input[type="number"], .stTextInput input {
    background: rgba(30,41,59,0.8) !important;
    border: 1px solid #1e293b !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 0.9rem !important;
    transition: border-color 0.2s !important;
}
input[type="number"]:focus { border-color: #38bdf8 !important; outline: none !important; }

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: rgba(30,41,59,0.8) !important;
    border: 1px solid #1e293b !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSelectbox"] > div > div:hover { border-color: #334155 !important; }

/* Dropdown menu */
[data-testid="stSelectbox"] ul {
    background: #0f1729 !important;
    border: 1px solid #1e293b !important;
    border-radius: 10px !important;
}
[data-testid="stSelectbox"] li { color: #cbd5e1 !important; }
[data-testid="stSelectbox"] li:hover { background: #1e293b !important; }

/* Slider */
[data-testid="stSlider"] > div > div > div > div {
    background: linear-gradient(90deg, #38bdf8, #818cf8) !important;
}
[data-testid="stSlider"] .st-bx { background: #1e293b !important; }

/* Slider thumb */
[data-testid="stSlider"] [role="slider"] {
    background: #38bdf8 !important;
    border: 2px solid #090b10 !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.25) !important;
}

/* Slider value text */
[data-testid="stSlider"] > div > div > div:last-child {
    color: #38bdf8 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
}

/* ── Predict button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    padding: 0.85rem 2.5rem !important;
    width: 100% !important;
    margin-top: 1rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 4px 24px rgba(14,165,233,0.25) !important;
}
[data-testid="stButton"] > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 32px rgba(14,165,233,0.35) !important;
}
[data-testid="stButton"] > button:active { transform: translateY(0) !important; }

/* ── Result cards ── */
.result-wrap {
    border-radius: 16px;
    padding: 2.2rem 2rem;
    margin-top: 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.result-churn {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.25);
}
.result-safe {
    background: rgba(34,197,94,0.07);
    border: 1px solid rgba(34,197,94,0.2);
}
.result-icon { font-size: 2.8rem; margin-bottom: 0.6rem; }
.result-label {
    font-family: 'Syne', sans-serif;
    font-size: 1.35rem;
    font-weight: 800;
    margin-bottom: 0.4rem;
}
.result-churn .result-label { color: #f87171; }
.result-safe .result-label { color: #4ade80; }
.result-desc { font-size: 0.88rem; color: #64748b; }

/* ── Probability bar ── */
.prob-bar-wrap { margin: 1.6rem 0 0.5rem; }
.prob-bar-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    color: #64748b;
    margin-bottom: 0.45rem;
    font-family: 'DM Sans', sans-serif;
    letter-spacing: 0.03em;
}
.prob-bar-track {
    height: 8px;
    background: #1e293b;
    border-radius: 99px;
    overflow: hidden;
}
.prob-bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.8s cubic-bezier(.4,0,.2,1);
}
.prob-churn { background: linear-gradient(90deg, #f87171, #ef4444); }
.prob-safe  { background: linear-gradient(90deg, #4ade80, #22c55e); }

/* ── Stat chip ── */
.stat-chips {
    display: flex;
    gap: 0.8rem;
    justify-content: center;
    margin-top: 1.2rem;
    flex-wrap: wrap;
}
.chip {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 99px;
    padding: 0.4rem 1rem;
    font-size: 0.78rem;
    color: #94a3b8;
    font-family: 'DM Sans', sans-serif;
}
.chip span { color: #e2e8f0; font-weight: 500; }

/* Streamlit success/error override — hide default */
[data-testid="stAlert"] { display: none !important; }

/* Hide default streamlit elements */
footer { display: none !important; }
#MainMenu { display: none !important; }

/* ── Metric row ── */
.metric-row {
    display: flex; gap: 1rem; margin-bottom: 1.2rem;
}
.metric-box {
    flex: 1;
    background: rgba(15,23,42,0.7);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-box .m-val {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: #38bdf8;
}
.metric-box .m-lbl {
    font-size: 0.72rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.2rem;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">AI-Powered Analytics</div>
    <h1>ChurnSense</h1>
    <p class="hero-sub">Predict customer churn risk with machine learning precision</p>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

# ── Load model ──
@st.cache_resource
def load_model():
    return joblib.load("churn_model.pkl")

model = load_model()

# ═══════════════════════════════
#  FORM — three column layout
# ═══════════════════════════════

st.markdown('<div class="section-label">Account Details</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    tenure = st.slider("Tenure (months)", 0, 72, 12)
with col2:
    MonthlyCharges = st.number_input("Monthly Charges (₹)", 0.0, 5000.0, 1000.0, step=50.0)
with col3:
    TotalCharges = st.number_input("Total Charges (₹)", 0.0, 10000.0, 2000.0, step=100.0)

avg_monthly_spend = TotalCharges / (tenure + 1)

# ── Live metric chips ──
st.markdown(f"""
<div class="metric-row">
    <div class="metric-box">
        <div class="m-val">₹{avg_monthly_spend:,.0f}</div>
        <div class="m-lbl">Avg Monthly Spend</div>
    </div>
    <div class="metric-box">
        <div class="m-val">{tenure}mo</div>
        <div class="m-lbl">Customer Tenure</div>
    </div>
    <div class="metric-box">
        <div class="m-val">₹{MonthlyCharges:,.0f}</div>
        <div class="m-lbl">Monthly Charges</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Demographics</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
with col2:
    SeniorCitizen = st.selectbox("Senior Citizen", [0, 1], format_func=lambda x: "Yes" if x else "No")
with col3:
    Partner = st.selectbox("Partner", [0, 1], format_func=lambda x: "Yes" if x else "No")
with col4:
    Dependents = st.selectbox("Dependents", [0, 1], format_func=lambda x: "Yes" if x else "No")

st.markdown('<div class="section-label">Services</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    PhoneService = st.selectbox("Phone Service", [0, 1], format_func=lambda x: "Yes" if x else "No")
    MultipleLines = st.selectbox("Multiple Lines", ["No", "Yes"])
    InternetService = st.selectbox("Internet Service", ["DSL", "Fiber optic", "NoInternet"])
with col2:
    OnlineSecurity = st.selectbox("Online Security", ["No", "Yes"])
    OnlineBackup = st.selectbox("Online Backup", ["No", "Yes"])
    DeviceProtection = st.selectbox("Device Protection", ["No", "Yes"])
with col3:
    TechSupport = st.selectbox("Tech Support", ["No", "Yes"])
    StreamingTV = st.selectbox("Streaming TV", ["No", "Yes"])
    StreamingMovies = st.selectbox("Streaming Movies", ["No", "Yes"])

st.markdown('<div class="section-label">Billing & Contract</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
with col2:
    PaymentMethod = st.selectbox("Payment Method", [
        "Electronic check", "Mailed check",
        "Bank transfer (automatic)", "Credit card (automatic)"
    ])
with col3:
    PaperlessBilling = st.selectbox("Paperless Billing", [0, 1], format_func=lambda x: "Yes" if x else "No")

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════
#  PREDICT
# ═══════════════════════════════
if st.button("⚡  Analyse Churn Risk"):
    input_data = pd.DataFrame([{
        "tenure": tenure,
        "MonthlyCharges": MonthlyCharges,
        "TotalCharges": TotalCharges,
        "avg_monthly_spend": avg_monthly_spend,
        "gender": gender,
        "SeniorCitizen": SeniorCitizen,
        "Partner": Partner,
        "Dependents": Dependents,
        "PhoneService": PhoneService,
        "PaperlessBilling": PaperlessBilling,
        "MultipleLines": MultipleLines,
        "InternetService": InternetService,
        "OnlineSecurity": OnlineSecurity,
        "OnlineBackup": OnlineBackup,
        "DeviceProtection": DeviceProtection,
        "TechSupport": TechSupport,
        "Contract": Contract,
        "PaymentMethod": PaymentMethod,
        "StreamingTV": StreamingTV,
        "StreamingMovies": StreamingMovies
    }])

    prob = model.predict_proba(input_data)[0][1]
    prediction = int(prob >= 0.35)
    pct = int(prob * 100)
    bar_cls = "prob-churn" if prediction == 1 else "prob-safe"

    if prediction == 1:
        st.markdown(f"""
        <div class="result-wrap result-churn">
            <div class="result-icon">⚠️</div>
            <div class="result-label">High Churn Risk</div>
            <div class="result-desc">This customer shows strong signals of churning. Consider a retention offer.</div>
            <div class="prob-bar-wrap">
                <div class="prob-bar-label">
                    <span>Churn probability</span>
                    <span style="color:#f87171;font-weight:600;">{pct}%</span>
                </div>
                <div class="prob-bar-track">
                    <div class="prob-bar-fill {bar_cls}" style="width:{pct}%"></div>
                </div>
            </div>
            <div class="stat-chips">
                <div class="chip">Risk Score <span>{prob:.3f}</span></div>
                <div class="chip">Threshold <span>0.35</span></div>
                <div class="chip">Tenure <span>{tenure}mo</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-wrap result-safe">
            <div class="result-icon">✅</div>
            <div class="result-label">Low Churn Risk</div>
            <div class="result-desc">This customer is likely to stay. Keep delivering value to maintain loyalty.</div>
            <div class="prob-bar-wrap">
                <div class="prob-bar-label">
                    <span>Churn probability</span>
                    <span style="color:#4ade80;font-weight:600;">{pct}%</span>
                </div>
                <div class="prob-bar-track">
                    <div class="prob-bar-fill {bar_cls}" style="width:{pct}%"></div>
                </div>
            </div>
            <div class="stat-chips">
                <div class="chip">Risk Score <span>{prob:.3f}</span></div>
                <div class="chip">Threshold <span>0.35</span></div>
                <div class="chip">Tenure <span>{tenure}mo</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)