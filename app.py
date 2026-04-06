from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path

app = FastAPI()

# Lazy load model to avoid version conflicts at startup
_model = None

def get_model():
    global _model
    if _model is None:
        model_path = Path(__file__).parent / "churn_model.pkl"
        _model = joblib.load(model_path)
    return _model

# Define input schema
class Customer(BaseModel):
    tenure: int
    MonthlyCharges: float
    TotalCharges: float
    avg_monthly_spend: float

    gender: str
    SeniorCitizen: int
    Partner: int
    Dependents: int
    PhoneService: int
    PaperlessBilling: int

    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str

    Contract: str
    PaymentMethod: str

    StreamingTV: str
    StreamingMovies: str


@app.post("/predict")
def predict(data: Customer):
    model = get_model()
    df = pd.DataFrame([data.dict()])

    prob = model.predict_proba(df)[0][1]

    threshold = 0.35
    prediction = int(prob >= threshold)

    return {
        "churn_probability": float(prob),
        "prediction": prediction
    }