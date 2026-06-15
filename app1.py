import streamlit as st
import numpy as np
import joblib
import time

# ==========================================
# LOAD TRAINED MODEL
# ==========================================

model = joblib.load("soil_model.pkl")

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Soil Recovery System",
    page_icon="🌱",
    layout="wide"
)

# ==========================================
# FUTURISTIC CSS
# ==========================================

st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(to right, #0f2027, #203a43, #2c7744);
    color: white;
}

/* Title */
h1 {
    text-align: center;
    color: #90EE90;
}

/* Input Labels Fix */
label {
    color: white !important;
    font-size: 18px !important;
    font-weight: bold !important;
}

/* Input box text */
input {
    color: black !important;
    font-size: 16px !important;
}

/* Buttons */
div.stButton > button {
    background-color: #00c853;
    color: white;
    border-radius: 12px;
    height: 55px;
    width: 100%;
    font-size: 22px;
    border: none;
    font-weight: bold;
}

div.stButton > button:hover {
    background-color: #00e676;
}

/* Section headers */
h2, h3 {
    color: #90EE90 !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SOIL ANALYSIS FUNCTION
# ==========================================

def detailed_soil_analysis(sample_data, soil_status):

    recommendations = []
    causes = []
    plants = []

    N = sample_data["N"]
    P = sample_data["P"]
    K = sample_data["K"]
    ph = sample_data["ph"]
    rainfall = sample_data["rainfall"]
    temperature = sample_data["temperature"]
    humidity = sample_data["humidity"]

    # ======================================
    # ROOT CAUSE ANALYSIS
    # ======================================

    if N < 40:
        causes.append("Nitrogen deficiency detected")
        recommendations.append(
            "Add nitrogen-rich compost or organic manure."
        )

    elif N > 100:
        causes.append("Excess nitrogen detected")
        recommendations.append(
            "Reduce nitrogen fertilizer usage."
        )

    if P < 40:
        causes.append("Low phosphorus detected")
        recommendations.append(
            "Apply phosphorus fertilizer or bone meal."
        )

    elif P > 100:
        causes.append("Excess phosphorus detected")
        recommendations.append(
            "Avoid over-fertilization."
        )

    if K < 40:
        causes.append("Low potassium detected")
        recommendations.append(
            "Add potassium-rich compost."
        )

    elif K > 100:
        causes.append("Excess potassium detected")
        recommendations.append(
            "Reduce potassium fertilizer usage."
        )

    if ph < 5.5:
        causes.append("Acidic soil condition")
        recommendations.append(
            "Apply lime treatment to increase pH."
        )

    elif ph > 7.5:
        causes.append("Alkaline soil condition")
        recommendations.append(
            "Apply sulfur treatment to reduce pH."
        )

    if rainfall < 50:
        causes.append("Low rainfall stress")
        recommendations.append(
            "Improve irrigation and water retention."
        )

    elif rainfall > 250:
        causes.append("Excess rainfall stress")
        recommendations.append(
            "Improve drainage system."
        )

    if temperature > 35:
        causes.append("High temperature stress")
        recommendations.append(
            "Use mulching to reduce heat stress."
        )

    elif temperature < 15:
        causes.append("Low temperature stress")
        recommendations.append(
            "Use temperature-resistant crops."
        )

    if humidity > 85:
        causes.append("High humidity fungal risk")
        recommendations.append(
            "Improve ventilation."
        )

    elif humidity < 30:
        causes.append("Low humidity stress")
        recommendations.append(
            "Increase irrigation frequency."
        )

    # ======================================
    # PREDICTION ALIGNED STRATEGY
    # ======================================

    if soil_status == "Poor":

        recommendations.insert(
            0,
            "Critical soil condition detected. Immediate recovery required."
        )

        recommendations.append(
            "Practice crop rotation for soil recovery."
        )

        recommendations.append(
            "Perform advanced soil testing."
        )

        plants.extend([
            "Clover",
            "Mustard",
            "Sunflower"
        ])

    elif soil_status == "Moderate":

        recommendations.insert(
            0,
            "Soil condition is moderate. Preventive correction recommended."
        )

        recommendations.append(
            "Monitor nutrient levels regularly."
        )

        recommendations.append(
            "Use organic fertilizers in controlled quantity."
        )

        plants.extend([
            "Legumes",
            "Cover Crops"
        ])

    else:

        recommendations.insert(
            0,
            "Soil ecosystem is healthy."
        )

        recommendations.append(
            "Maintain sustainable farming practices."
        )

        recommendations.append(
            "Continue regular soil monitoring."
        )

        plants.extend([
            "Main Crops",
            "Crop Rotation"
        ])

    # Hidden pattern detection
    if soil_status == "Poor" and len(causes) == 0:
        causes.append(
            "Hidden environmental imbalance detected by AI model"
        )

    # Remove duplicates
    plants = list(set(plants))
    recommendations = list(dict.fromkeys(recommendations))

    return causes, recommendations, plants


# ==========================================
# TITLE
# ==========================================

st.title("🌱 AI-Driven Adaptive Soil Health Recovery System")

st.markdown("### Enter Soil Parameters")

# ==========================================
# INPUT FIELDS
# ==========================================

col1, col2 = st.columns(2)

with col1:
    N = st.number_input("Nitrogen (N)", 0, 150, 50)
    P = st.number_input("Phosphorus (P)", 0, 150, 50)
    K = st.number_input("Potassium (K)", 0, 200, 50)
    temp = st.number_input("Temperature (°C)", 0.0, 50.0, 25.0)

with col2:
    humidity = st.number_input("Humidity (%)", 0.0, 100.0, 50.0)
    ph = st.number_input("pH Level", 0.0, 14.0, 6.5)
    rainfall = st.number_input("Rainfall (mm)", 0.0, 300.0, 100.0)

# ==========================================
# PREDICT BUTTON
# ==========================================

if st.button("🚀 Predict Soil Health"):

    with st.spinner("Predicting Soil Health... 🌱"):
        time.sleep(2)

        # Create input sample
        sample = np.array([
            [N, P, K, temp, humidity, ph, rainfall]
        ])

        # Prediction
        prediction = model.predict(sample)[0]

        # Correct label mapping
        labels = ["Healthy", "Moderate", "Poor"]
        soil_status = labels[prediction]

    # Show prediction
    st.success(f"✅ Predicted Soil Health: {soil_status}")

    # Dictionary for analysis
    sample_data = {
        "N": N,
        "P": P,
        "K": K,
        "ph": ph,
        "rainfall": rainfall,
        "temperature": temp,
        "humidity": humidity
    }

    # Get analysis
    causes, recommendations, plants = detailed_soil_analysis(
        sample_data,
        soil_status
    )

    # ======================================
    # ROOT CAUSE ANALYSIS
    # ======================================

    st.subheader("🔍 Root Cause Analysis")

    if causes:
        for cause in causes:
            st.write("✔", cause)
    else:
        st.write("✔ No major issues detected.")

    # ======================================
    # PLANT RECOMMENDATIONS
    # ======================================

    st.subheader("🌻 Recommended Recovery Plants")

    for plant in plants:
        st.write("✔", plant)

    # ======================================
    # TREATMENT PLAN
    # ======================================

    st.subheader("🛠 Treatment Plan")

    for rec in recommendations:
        st.write("✔", rec)