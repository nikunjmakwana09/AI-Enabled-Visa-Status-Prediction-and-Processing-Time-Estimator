import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field, validator
from app.estimator_engine import estimate_processing_time
from typing import Optional, Dict, Any

MODEL_REPORT_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "model_report.json")

_model_report = {}
try:
    import json
    with open(os.path.abspath(MODEL_REPORT_PATH), "r") as f:
        _model_report = json.load(f)
except Exception:
    _model_report = {}

load_dotenv()

API_KEY = os.getenv("API_KEY")

app = FastAPI(
    title="AI Visa Status Prediction and Processing Time Estimator API",
    description="API endpoint for predicting visa processing time.",
    version="1.0"
)


class VisaRequest(BaseModel):
    fiscal_year: int = Field(..., ge=2000, le=2100)
    application_month: int = Field(..., ge=1, le=12)
    region: str = Field(..., min_length=2, max_length=3)
    processing_office: str = Field(..., min_length=1, max_length=20)
    visa_type: str = Field(..., min_length=1, max_length=50)

    @validator("region")
    def normalize_region(cls, v):
        return v.strip().upper()

    @validator("visa_type")
    def normalize_visa_type(cls, v):
        return v.strip()


class VisaPredictionResponse(BaseModel):
    status: str
    prediction_days: float
    confidence_interval: list[float]
    confidence_score: float
    benchmark_mae: float
    residual_interval: list[float]
    extra: Optional[Dict[str, Any]] = None


def verify_api_key(x_api_key: str = Header(...)):

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )

    return x_api_key


@app.get("/")
def root():

    return {
        "status": "Welcome to the AI Visa Prediction API",
        "service": "Visa processing Prediction Engine"
    }


@app.post("/predict", response_model=VisaPredictionResponse)
def predict(
    request: VisaRequest,
    api_key: str = Depends(verify_api_key)
):

    data = request.dict()

    quarter = (data["application_month"] - 1) // 3 + 1
    season_index = 1 if data["application_month"] in [12, 1, 2] else 0

    # baseline defaults; in production, replace with real dynamic metrics
    data.update({
        "application_quarter": quarter,
        "application_year": data["fiscal_year"],
        "region_avg_time": 610.0,
        "office_avg_time": 600.0,
        "office_volume": 300.0,
        "season_index": season_index,
        "office_pressure": 300.0 / 600.0
    })

    result = estimate_processing_time(data)

    if result.get("status") != "success":
        raise HTTPException(status_code=500, detail=result.get("message", "Unknown error"))

    return result


@app.get("/health")
def health():
    return {
        "status": "AI Visa Prediction API running",
        "service": "Prediction Engine",
        "model_type": _model_report.get("final_model", "unknown"),
        "model_mae": _model_report.get("final_metrics", {}).get("mae"),
        "debug": {
            "has_model_report": bool(_model_report)
        }
    }
