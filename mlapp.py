import streamlit as st
import joblib
import pandas as pd

st.set_page_config(page_title="Maternal Health Risk", page_icon="🤰", layout="centered")

st.markdown("""
<style>
    .title { color: #6a3093; text-align: center; font-size: 3rem !important; font-weight: 700; }
    .subtitle { color: #7b7b7b; text-align: center; font-size: 1.2rem !important; margin-bottom: 2rem; }
    .result-box { padding: 2.5rem; border-radius: 12px; margin: 2rem 0; text-align: center; 
                font-size: 2rem !important; font-weight: 700; box-shadow: 0 6px 18px rgba(0,0,0,0.12); }
    .low-risk { background: #e8f5e9 !important; border: 5px solid #2e7d32 !important; color: #1b5e20 !important; }
    .medium-risk { background: #fff8e1 !important; border: 5px solid #ff8f00 !important; color: #e65100 !important; }
    .high-risk { background: #ffebee !important; border: 5px solid #c62828 !important; color: #b71c1c !important; }
    .recommendation { padding: 1.5rem; margin: 1.5rem 0; border-radius: 10px; font-size: 1.2rem !important;
                     box-shadow: 0 4px 12px rgba(0,0,0,0.1); display: flex; align-items: center; gap: 15px;
                     color: #2c3e50 !important; }  /* Added dark text color */
    .recommendation-low { background: #e8f5e9 !important; border-left: 6px solid #2e7d32 !important; }
    .recommendation-medium { background: #fff8e1 !important; border-left: 6px solid #ff8f00 !important; }
    .recommendation-high { background: #ffebee !important; border-left: 6px solid #c62828 !important; 
                          color: #b71c1c !important; font-weight: 700 !important; }
    .rec-icon { font-size: 2rem !important; min-width: 40px; }
    .high-risk-icon { color: #c62828 !important; }
    .input-label { font-size: 1.2rem !important; font-weight: 600 !important; color: #2c3e50 !important; }
    .footer { text-align: center; color: #7f8c8d; margin-top: 3rem; padding: 1.5rem; border-top: 1px solid #eee; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">MATERNAL HEALTH RISK ASSESSMENT</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Instant pregnancy health evaluation</div>', unsafe_allow_html=True)

try:
    model = joblib.load('maternal_risk_model.pkl')
except:
    st.error("Model not loaded. Please check model file.")
    st.stop()

with st.form("health_form"):
    st.markdown("### Patient Health Information")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="input-label">Age (years)</p>', unsafe_allow_html=True)
        age = st.number_input("", 15, 50, 25, label_visibility="collapsed")
        st.markdown('<p class="input-label">Systolic BP (mmHg)</p>', unsafe_allow_html=True)
        systolic_bp = st.number_input("", 70, 200, 120, label_visibility="collapsed")
        st.markdown('<p class="input-label">Diastolic BP (mmHg)</p>', unsafe_allow_html=True)
        diastolic_bp = st.number_input("", 40, 120, 80, label_visibility="collapsed")
    with col2:
        st.markdown('<p class="input-label">Blood Sugar (mmol/L)</p>', unsafe_allow_html=True)
        bs = st.number_input("", 3.0, 20.0, 5.0, step=0.1, label_visibility="collapsed")
        st.markdown('<p class="input-label">Body Temp (°F)</p>', unsafe_allow_html=True)
        body_temp = st.number_input("", 95.0, 105.0, 98.6, step=0.1, label_visibility="collapsed")
        st.markdown('<p class="input-label">Heart Rate (bpm)</p>', unsafe_allow_html=True)
        heart_rate = st.number_input("", 50, 140, 75, label_visibility="collapsed")
    submitted = st.form_submit_button("CHECK RISK LEVEL", type="primary")

if submitted:
    input_data = pd.DataFrame([[age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate]], 
                            columns=['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate'])
    prediction = model.predict(input_data)[0]
    risk_levels = {
        0: {"name": "MIN RISK", "class": "min-risk", "icon": "✅", "rec_class": "recommendation-min"},
        1: {"name": "MID RISK", "class": "mid-risk", "icon": "⚠️", "rec_class": "recommendation-mid"},
        2: {"name": "MAX RISK", "class": "max-risk", "icon": "🚨", "rec_class": "recommendation-max"}
    }
    risk = risk_levels[prediction]
    st.markdown(f'<div class="result-box {risk["class"]}"><h2>{risk["icon"]} {risk["name"]}</h2></div>', unsafe_allow_html=True)
    st.markdown("### Recommended Actions")
    if prediction == 0:
        st.markdown(f'<div class="recommendation {risk["rec_class"]}"><span class="rec-icon">📅</span><span style="color: #2c3e50 !important;">Continue regular prenatal checkups</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="recommendation {risk["rec_class"]}"><span class="rec-icon">🍎</span><span style="color: #2c3e50 !important;">Maintain balanced nutrition</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="recommendation {risk["rec_class"]}"><span class="rec-icon">🏃‍♀️</span><span style="color: #2c3e50 !important;">Light exercise recommended</span></div>', unsafe_allow_html=True)
    elif prediction == 1:
        st.markdown(f'<div class="recommendation {risk["rec_class"]}"><span class="rec-icon">🩺</span><span style="color: #2c3e50 !important;">Schedule additional monitoring</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="recommendation {risk["rec_class"]}"><span class="rec-icon">📊</span><span style="color: #2c3e50 !important;">Monitor BP twice daily</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="recommendation {risk["rec_class"]}"><span class="rec-icon">🚫</span><span style="color: #2c3e50 !important;">Reduce strenuous activities</span></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="recommendation {risk["rec_class"]}"><span class="rec-icon high-risk-icon">🚨</span><span style="color: #b71c1c !important; font-weight: 700 !important;">SEEK IMMEDIATE MEDICAL ATTENTION</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="recommendation {risk["rec_class"]}"><span class="rec-icon high-risk-icon">🏥</span><span style="color: #b71c1c !important;">Prepare for hospitalization</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="recommendation {risk["rec_class"]}"><span class="rec-icon high-risk-icon">📞</span><span style="color: #b71c1c !important;">Have emergency contacts ready</span></div>', unsafe_allow_html=True)


st.markdown('<div class="footer">Note: This tool provides preliminary assessment only</div>', unsafe_allow_html=True)  
