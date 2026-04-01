import pandas as pd
import numpy as np
import logging
import joblib
import json
from typing import Dict, Any
from pathlib import Path


# ==========================================================
# Logging
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==========================================================
# Load Model
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "best_model.pkl"
PREPROCESSOR_PATH = BASE_DIR / "models" / "preprocessor.pkl"

try:
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    logging.info("Model and preprocessor loaded successfully.")

except Exception as e:
    logging.error(f"Model loading failed: {e}")
    raise RuntimeError("Model files not found. Check deployment paths.")


# ==========================================================
# Valid Inputs
# ==========================================================

VALID_REGIONS = ["AF", "AS", "EU", "OC", "SA"]


# ==========================================================
# Input Validation
# ==========================================================

def validate_input(user_input: Dict[str, Any]):

    if user_input.get("region") not in VALID_REGIONS:
        raise ValueError(f"Invalid region: {user_input.get('region')}")

    if not (1 <= user_input.get("application_month", 0) <= 12):
        raise ValueError("Application month must be between 1 and 12")

    if not isinstance(user_input.get("application_month"), int):
        raise ValueError("Application month must be an integer")

    if not isinstance(user_input.get("fiscal_year"), int):
        raise ValueError("Fiscal year must be an integer")


# ==========================================================
# Feature Preparation
# ==========================================================

def prepare_features(user_input):

    df = pd.DataFrame([user_input])

    feature_cols = [
        "fiscal_year",
        "application_month",
        "application_quarter",
        "application_year",
        "region",
        "processing_office",
        "visa_type",
        "region_avg_time",
        "office_avg_time",
        "office_volume",
        "season_index",
        "office_pressure",
        "office_rolling_30_mean",
        "office_rolling_30_std",
        "region_rolling_30_mean",
        "region_rolling_30_std",
        "office_mom_diff"
    ]

    # allow derived rolling stats defaults for sample requests; they should be provided in production
    required = [c for c in feature_cols if c not in df.columns]
    if required:
        logging.warning(f"Optional derived feature(s) missing, filling with 0: {required}")
        for c in required:
            df[c] = 0.0

    df = df[feature_cols].copy()

    # enforce types and cast
    df["fiscal_year"] = df["fiscal_year"].astype(int)
    df["application_month"] = df["application_month"].astype(int)
    df["application_quarter"] = df["application_quarter"].astype(int)
    df["application_year"] = df["application_year"].astype(int)

    # Preprocess with pipeline saved during training
    feature_array = preprocessor.transform(df)

    return feature_array


# ==========================================================
# Predict Processing Time
# ==========================================================

def predict_processing_time(features):

    prediction = model.predict(features)

    return float(prediction[0])


# ==========================================================
# Model report, uncertainty and confidence helpers
# ==========================================================

MODEL_REPORT_PATH = BASE_DIR / "models" / "model_report.json"

try:
    with open(MODEL_REPORT_PATH, "r") as f:
        _model_report = json.load(f)
    logging.info("Model report loaded successfully.")
except Exception as e:
    _model_report = {}
    logging.warning(f"Could not load model report: {e}")

_residual_interval = _model_report.get("residual_interval_5_95", None)
_final_mae = _model_report.get("final_metrics", {}).get("mae", None)


def calculate_prediction_confidence():
    """Return a confidence score in [0,100] from historical validation MAE."""
    if _final_mae is None:
        return 60.0

    if _final_mae < 20:
        return 95.0
    if _final_mae < 40:
        return 85.0
    if _final_mae < 60:
        return 75.0

    return round(max(5, 100 - _final_mae), 1)


def calculate_confidence_interval(prediction):
    """Use training residual envelope if available, otherwise fallback to +/- 10%."""
    if _residual_interval is not None and len(_residual_interval) == 2:
        lower = prediction + _residual_interval[0]
        upper = prediction + _residual_interval[1]
    else:
        lower = prediction * 0.9
        upper = prediction * 1.1

    return round(max(0, float(lower)), 1), round(max(0, float(upper)), 1)


# ==========================================================
# Main Prediction Engine
# ==========================================================

def estimate_processing_time(user_input: Dict[str, Any]):

    try:

        logging.info(
            f"Prediction request | region={user_input.get('region')} | "
            f"office={user_input.get('processing_office')}"
        )

        validate_input(user_input)

        features = prepare_features(user_input)

        logging.info(f"Feature vector shape: {features.shape}")
        logging.info(f"Non-zero features: {np.count_nonzero(features)}")

        prediction = max(1.0, predict_processing_time(features))

        lower, upper = calculate_confidence_interval(prediction)
        confidence = calculate_prediction_confidence()

        logging.info(f"Predicted processing time: {prediction} days")

        return {
            "status": "success",
            "prediction_days": float(round(prediction, 1)),
            "confidence_interval": [float(round(lower, 1)), float(round(upper, 1))],
            "confidence_score": float(round(confidence, 1)),
            "benchmark_mae": float(_final_mae) if _final_mae is not None else None,
            "residual_interval": _residual_interval
        }

    except Exception as e:

        logging.error(f"Prediction failed: {str(e)}")

        return {
            "status": "error",
            "message": str(e)
        }
