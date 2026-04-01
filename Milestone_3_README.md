# AI-Enabled Visa Status Prediction & Processing Time Estimator

**Milestone 3 — Predictive Modeling**

### Objective

The goal of **Milestone 3** is to develop and evaluate machine learning models capable of predicting visa processing time.

This stage focuses on:

* training multiple regression models
* comparing model performance
* optimizing promising models through hyperparameter tuning
* interpreting model behavior using feature importance and SHAP explanations
* ensuring models are robust, scalable and aligned with real-world deployment scenarios
---

# Dataset

Milestone 3 uses the engineered dataset created in **Milestone 2**.

```
data/processed/engineered_dataset.csv
```

Dataset summary:

| Metric              | Value                                    |
| ------------------- | ---------------------------------------- |
| Records             | 50,135                                   |
| Engineered Features | Temporal + workload + trend-based metrics|
| Target Variable     | processing_time_days                     |

Categorical variables are encoded using one-hot encoding and numerical features are standardized using a preprocessing pipeline.
---

# Model Training Pipeline

The training pipeline is implemented in:

```
notebooks/scripts/model_training.py
```

### Steps in the Pipeline

01. Load engineered dataset
02. Select predictive features
03. Apply preprocessing (one-hot encoding + scaling using ColumnTransformer)
04. Perform time-aware train-test split (to avoid leakage)
05. Train baseline regression models
06. Compare model performance
07. Perform hyperparameter tuning
08. Evaluate tuned models
09. Apply cross-validation and walk-forward validation
11. Generate model explanations
10. Save the final trained model and metadata

---

# Baseline Models

Four regression models were trained and evaluated.

| Model               | Purpose                                 |
| ------------------- | --------------------------------------- |
| Linear Regression   | Baseline linear model                   |
| Random Forest       | Non-linear ensemble model               |
| Gradient Boosting   | Boosting-based regression               |
| HistGradientBoosting| Regularized gradient boosting (industry)|
| XGBoost             | Optimized gradient boosting model       |
| LightGBM (optional) | High-performance boosting model         |
| CatBoast (optional) | Categorical-aware boosting model        |

---

# Evaluation Metrics

Models were evaluated using standard regression metrics.

| Metric | Description                   |
| ------ | ----------------------------- |
| MAE    | Mean Absolute Error           |
| RMSE   | Root Mean Squared Error       |
| R²     | Coefficient of determination  |
| MAPE   | Mean Absolute Percentage Error|

These metrics measure prediction accuracy and model fit.

---

# Hyperparameter Tuning

Hyperparameter optimization was performed using **GridSearchCV**.

The tuning process searches for the best parameter combination that minimizes prediction error.

---

# Cross-Validation

Multiple validation strategies were applied:

```
TimeSeriesSplit (5 folds)
Standard Cross Validation
Walk-forward validation
```

This ensures robust performance and prevents temporal leakage.

---

# Advanced Modeling

### Stacking Ensemble Model

A stacking regressor was implemented combining:
Random Forest + XGBoost + LightGBM + CatBoost

The final selected model:
StackingRegressor

This model achieved the best performance among all candidates.

# Model Performance

From model report:
MAE  ≈ 58.53 days
RMSE ≈ 71.74 days
R²   ≈ 0.18
MAPE ≈ 10.55%

These results indicate stable performance on real-world visa processing data.

# Model Explainability

Two explainability techniques were used.

### Feature Importance

Feature importance was extracted from the **Random Forest model** to identify the most influential predictors.

Output:

```
plots/random_forest_feature_importance.png
```

---

### SHAP Analysis

Model interpretability was further improved using **SHAP (SHapley Additive Explanations)**.

SHAP values explain how each feature influences individual predictions of the XGBoost model.

Output:

```
plots/xgboost_shap_summary.png
```

---

# Model Outputs

### Saved Model

```
models/best_model.pkl
```

---

### Preprocessing Pipeline

```
models/preprocessor.pkl
```

---

### Feature Schema

```
models/feature_schema.json
```

---

### Model Reports & Metadata

```
models/model_report.json
models/model_metadata.json
models/drift_report.json
```

These include:
• model performance metrics
• dataset hash for reproducibility
• training configuration
• feature drift analysis

---

### Drift Detection

Statistical drift analysis was performed using KS-test between training and test data.

This ensures:
• detection of distribution changes
• monitoring model reliability in production

---

### Prediction Uncertainty

A residual-based confidence interval is generated:
90% prediction interval

This provides:
• lower and upper bounds
• uncertainty estimation for predictions

---

### Generated Plots

```
plots/
 ├── random_forest_feature_importance.png
 └── xgboost_shap_summary.png
```

---

# Project Structure (Milestone 3)

```
notebooks/scripts/
 └── model_training.py

models/
 ├── best_model.pkl
 ├── preprocessor.pkl
 ├── feature_schema.json
 ├── model_report.json
 ├── model_metadata.json
 └── drift_report.json

plots/
 ├── random_forest_feature_importance.png
 └── xgboost_shap_summary.png
```

---

# Outcome

✔ Multiple regression models trained
✔ Best model selected using performance comparison
✔ Hyperparameter tuning applied
✔ Time-aware validation implemented
✔ Stacking ensemble model deployed
✔ Model explainability enabled (SHAP + feature importance)
✔ Production artifacts generated (model + metadata + drift report)
✔ Prediction uncertainty integrated

The trained model is now ready for **deployment and prediction of visa processing times in Milestone 4**.
