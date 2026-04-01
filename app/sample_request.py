from estimator_engine import estimate_processing_time


# ==========================================================
# Sample User Input
# ==========================================================

sample_input = {

    "fiscal_year": 2024,
    "application_month": 5,
    "application_quarter": 2,
    "application_year": 2024,

    "region": "AS",
    "processing_office": "NWD",
    "visa_type": "DV_Lottery",

    "region_avg_time": 610,
    "office_avg_time": 600,
    "office_volume": 300,

    "season_index": 0,
    "office_pressure": 0.5
}


# ==========================================================
# Run Prediction
# ==========================================================

result = estimate_processing_time(sample_input)

print("\nPrediction Result")

if result["status"] == "success":

    print("Estimated Processing Time:",
          result["prediction_days"], "days")

    print("Confidence Interval:",
          result["confidence_interval"][0],
          "-",
          result["confidence_interval"][1],
          "days")

else:

    print("Error:", result["message"])
