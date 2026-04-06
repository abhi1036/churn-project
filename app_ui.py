import streamlit as st
import joblib
import pandas as pd

# Load model
model = joblib.load("churn_model.pkl")

st.title("Customer Churn Prediction")

st.write("Enter customer details:")

# Inputs
tenure = st.slider("Tenure (months)", 0, 72, 12)
MonthlyCharges = st.number_input("Monthly Charges", 0.0, 5000.0, 1000.0)
TotalCharges = st.number_input("Total Charges", 0.0, 10000.0, 2000.0)

avg_monthly_spend = TotalCharges / (tenure + 1)

gender = st.selectbox("Gender", ["Male", "Female"])
SeniorCitizen = st.selectbox("Senior Citizen", [0, 1])
Partner = st.selectbox("Partner", [0, 1])
Dependents = st.selectbox("Dependents", [0, 1])
PhoneService = st.selectbox("Phone Service", [0, 1])
PaperlessBilling = st.selectbox("Paperless Billing", [0, 1])

MultipleLines = st.selectbox("Multiple Lines", ["No", "Yes"])
InternetService = st.selectbox("Internet Service", ["DSL", "Fiber optic", "NoInternet"])
OnlineSecurity = st.selectbox("Online Security", ["No", "Yes"])
OnlineBackup = st.selectbox("Online Backup", ["No", "Yes"])
DeviceProtection = st.selectbox("Device Protection", ["No", "Yes"])
TechSupport = st.selectbox("Tech Support", ["No", "Yes"])

Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
PaymentMethod = st.selectbox("Payment Method", [
    "Electronic check",
    "Mailed check",
    "Bank transfer (automatic)",
    "Credit card (automatic)"
])

StreamingTV = st.selectbox("Streaming TV", ["No", "Yes"])
StreamingMovies = st.selectbox("Streaming Movies", ["No", "Yes"])

# Predict button
if st.button("Predict Churn"):

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

    st.subheader("Result")

    st.write(f"Churn Probability: {prob:.2f}")

    if prediction == 1:
        st.error("Customer is likely to churn")
    else:
        st.success("Customer is not likely to churn")