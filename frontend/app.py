import os
import requests
import streamlit as st
from dotenv import load_dotenv

# load .env to env vars
load_dotenv()

API_URL = os.getenv("API_URL")

st.set_page_config(
    page_title="MediMate.ML",
    page_icon="⚕️",
    layout="centered"
)

st.title("⚕️ MediMate.ML")
st.write("Heart Disease Risk Predictor")

st.subheader("Enter patient details and click **Predict**")

def coded_choice(label, choices, default_code):
    """Show readable category labels while sending the dataset's integer code."""
    labels = [f"{description} (code {code})" for code, description in choices]
    default_index = next(i for i, (code, _) in enumerate(choices) if code == default_code)
    selected = st.selectbox(label, labels, index=default_index)
    return choices[labels.index(selected)][0]

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age", 1, 120, 52)
    sex = st.selectbox("Sex (1 = Male, 0 = Female)", [0, 1])
    cp = coded_choice("Chest Pain Type (cp)", [
        (0, "Typical angina"),
        (1, "Atypical angina"),
        (2, "Non-anginal pain"),
        (3, "Asymptomatic"),
    ], 0)
    trestbps = st.number_input("Resting Blood Pressure", 0, 250, 125)
    chol = st.number_input("Cholesterol", 0, 600, 212)


with col2:
    fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1])
    restecg = coded_choice("Resting ECG (restecg)", [
        (0, "Normal"),
        (1, "ST-T wave abnormality"),
        (2, "Left ventricular hypertrophy"),
    ], 1)
    thalach = st.number_input("Max Heart Rate (thalach)", 0, 250, 168)
    exang = st.selectbox("Exercise Induced Angina", [0, 1])


with col3:
    oldpeak = st.number_input("Oldpeak (ST depression)", 0.0, 10.0, 1.0)
    slope = coded_choice("Slope of peak exercise ST segment (slope)", [
        (0, "Downsloping"),
        (1, "Flat"),
        (2, "Upsloping"),
    ], 2)
    ca = st.number_input("Number of Major Vessels (ca)", 0, 4, 0)
    thal = coded_choice("Thal (dataset code)", [
        (0, "Normal"),
        (1, "Fixed defect"),
        (2, "Reversible defect"),
        (3, "Unknown"),
    ], 2)

if st.button("🔍 Predict"):
    input_data = {
        "age": age,
        "sex": sex,
        "cp": cp,
        "trestbps": trestbps,
        "chol": chol,
        "fbs": fbs,
        "restecg": restecg,
        "thalach": thalach,
        "exang": exang,
        "oldpeak": oldpeak,
        "slope": slope,
        "ca": ca,
        "thal": thal
    }

    response = requests.post(API_URL, json=input_data)

    if response.status_code != 200:
        st.error("Something went wrong. Try again later...")
    
    else:
        result = response.json()
        prediction = result["prediction"]
        probability = result["probability"]
        diagnosis = result["diagnosis"]

        st.divider()

        st.metric(
            label="Heart Disease Probability",
            value=f"{probability:.2f}"
        )

        if prediction == 1:
            st.error(f"⚠️Model Prediction: {diagnosis}")
        else:
            st.success(f"✅ Model Prediction: {diagnosis}")
