import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Early-Warning System for Aadhaar Service Disruptions")

# -------------------------
# 1. LOAD DATA
# -------------------------
trend_file = st.file_uploader("Upload Usage Trend CSV", type="csv")
bio_file = st.file_uploader("Upload Biometric CSV", type="csv")
otp_file = st.file_uploader("Upload OTP CSV (with Demographics)", type="csv")
aua_file = st.file_uploader("Upload Top AUA CSV", type="csv")
asa_file = st.file_uploader("Upload Top ASA CSV", type="csv")

risk = None  # initialize risk variable

# -------------------------
# 2. RISK DETECTION
# -------------------------
if trend_file is not None:
    trend = pd.read_csv(trend_file)
    trend.columns = ["Time", "Value"]

    avg = trend["Value"].mean()
    latest = trend["Value"].iloc[-1]

    st.subheader("Aadhaar Usage Trend")

    fig, ax = plt.subplots()
    ax.plot(trend["Time"], trend["Value"], marker="o")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    p75 = trend["Value"].quantile(0.75)
    p90 = trend["Value"].quantile(0.90)

    if latest > p90:
        risk = "HIGH"
        st.error("🔴 HIGH RISK: Extreme Load Detected")
    elif latest > p75:
        risk = "MEDIUM"
        st.warning("🟡 MEDIUM RISK: Above Normal Load")
    else:
        risk = "LOW"
        st.success("🟢 LOW RISK: Normal Usage")

# -------------------------
# RISK-BASED RECOMMENDATION
# -------------------------
if risk == "HIGH":
    st.info("🔁 Recommendation: Prefer OTP authentication to reduce biometric stress")
elif risk == "MEDIUM":
    st.info("⚠️ Recommendation: Use OTP for non‑critical services")
elif risk == "LOW":
    st.info("✅ Biometric authentication is safe")

# -------------------------
# 3. AUTH TYPE DECISION
# -------------------------
if bio_file is not None and otp_file is not None:
    bio = pd.read_csv(bio_file)
    otp = pd.read_csv(otp_file)

    bio.columns = ["Time", "Bio_Value"]

    bio_avg = bio["Bio_Value"].mean()
    otp_avg = otp.iloc[:, 1].mean()

    st.subheader("Recommended Authentication Type")

    if bio_avg > otp_avg:
        st.info("✅ Prefer OTP authentication during high load")
    else:
        st.info("✅ Biometric authentication is stable")

# -------------------------
# 4. DEMOGRAPHIC INSIGHT
# -------------------------
if otp_file is not None:
    st.subheader("OTP Demographic Insight")

    if "Age_Group" in otp.columns:
        demo = otp.groupby("Age_Group").sum().iloc[:, 0]
        st.bar_chart(demo)
        st.write("👉 Elderly and mobile‑enabled groups benefit more from OTP")

# -------------------------
# 5. AUA & ASA FOCUS
# -------------------------
st.subheader("🚨 Priority Attention Required")

if aua_file is not None:
    aua = pd.read_csv(aua_file)
    top_aua = aua.head(3)
    st.write("🔴 High‑Load AUAs:")
    st.table(top_aua)

if asa_file is not None:
    asa = pd.read_csv(asa_file)
    top_asa = asa.head(3)
    st.write("🔴 Critical ASAs:")
    st.table(top_asa)

# -------------------------
# 6. FINAL ACTION
# -------------------------
st.subheader("Government Action Recommendation")

st.write("""
- Use OTP during high-risk periods  
- Stagger bulk AUA requests  
- Scale infrastructure for high-load ASAs  
- Protect vulnerable demographic groups  
""")
