import os
import json
import warnings
from datetime import datetime
import joblib
import hashlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import shap
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, HistGradientBoostingRegressor, StackingRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from scipy.stats import ks_2samp

# optional high-power libraries
try:
    import lightgbm as lgb
except ImportError:
    lgb = None

try:
    from catboost import CatBoostRegressor
except ImportError:
    CatBoostRegressor = None

warnings.filterwarnings("ignore")


# ==========================================================
# Create model folder
# ==========================================================

os.makedirs("models", exist_ok=True)


# ==========================================================
# Load dataset
# ==========================================================

df = pd.read_csv("data/processed/engineered_dataset.csv")

print("Dataset Loaded")
print("Shape:", df.shape)


# ==========================================================
# Feature selection
# ==========================================================

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
    "application_year_month",
    "office_rolling_30_mean",
    "office_rolling_30_std",
    "region_rolling_30_mean",
    "region_rolling_30_std",
    "office_mom_diff"
]

# Confirm dataset includes required features
missing_features = [c for c in feature_cols + ["processing_time_days"] if c not in df.columns]
if missing_features:
    raise ValueError(f"Missing expected features in dataset: {missing_features}")

# Drop direct case_status and derived status flags to avoid leakage from final disposition
drop_cols = [c for c in ["case_status", "Issued", "AP", "Ready", "Refused", "InTransit", "Transfer", "NVC", "Refused221g"] if c in df.columns]
if drop_cols:
    df = df.drop(columns=drop_cols)

# Keep a copy for diagnostics (for ensemble analyses or drift monitoring)
df_model = df[feature_cols + ["processing_time_days"]].copy()

# Outlier clip (already done in preprocessing) for extra safety
q_low = df_model["processing_time_days"].quantile(0.01)
q_high = df_model["processing_time_days"].quantile(0.99)
df_model = df_model[(df_model["processing_time_days"] >= q_low) & (df_model["processing_time_days"] <= q_high)]


# ==========================================================
# One-hot encoding + scaling pipeline
# ==========================================================

# Align train/test split by time to prevent leakage
if "application_date" in df.columns:
    df_ordered = df.sort_values("application_date").reset_index(drop=True)
else:
    df_ordered = df_model.copy()

X_raw = df_ordered[feature_cols]
y = df_ordered["processing_time_days"]

categorical_cols = ["region", "processing_office", "visa_type"]
numeric_cols = [
    "fiscal_year", "application_month", "application_quarter", "application_year",
    "region_avg_time", "office_avg_time", "office_volume", "season_index", "office_pressure",
    "office_rolling_30_mean", "office_rolling_30_std", "region_rolling_30_mean", "region_rolling_30_std", "office_mom_diff"
]

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols),
    ("num", StandardScaler(), numeric_cols)
], remainder="drop")

X_transformed = preprocessor.fit_transform(X_raw)

# Extract feature names for debugging and deployment
onehot_names = preprocessor.named_transformers_["cat"].get_feature_names_out(categorical_cols)
feature_schema = list(onehot_names) + numeric_cols

os.makedirs("models", exist_ok=True)
with open("models/feature_schema.json", "w") as f:
    json.dump(feature_schema, f)

# Save preprocessing pipeline for production
joblib.dump(preprocessor, "models/preprocessor.pkl")

print("Feature schema and preprocessor saved successfully.")

X = pd.DataFrame(X_transformed, columns=feature_schema)

print("Features after transformation:", X.shape)


# ==========================================================
# Train / Test Split (time-aware)
# ==========================================================

os.makedirs("models", exist_ok=True)

feature_schema = list(X.columns)

with open("models/feature_schema.json", "w") as f:
    json.dump(feature_schema, f)

print("Feature schema saved successfully.")


# ==========================================================
# Train / Test Split (time-series aware)
# ==========================================================

split_at = int(len(X) * 0.8)
X_train = X.iloc[:split_at].copy()
X_test = X.iloc[split_at:].copy()
y_train = y.iloc[:split_at].copy()
y_test = y.iloc[split_at:].copy()

print("Train Size:", X_train.shape)
print("Test Size:", X_test.shape)

# Basic overfitting/underfitting diagnostics
print("Train target distribution:", y_train.describe().to_dict())
print("Test target distribution:", y_test.describe().to_dict())


# ==========================================================
# Evaluation Function
# ==========================================================

def evaluate_model(name, model):

    model.fit(X_train, y_train)

    predictions_train = model.predict(X_train)
    predictions_test = model.predict(X_test)

    mae_train = mean_absolute_error(y_train, predictions_train)
    mae_test = mean_absolute_error(y_test, predictions_test)
    rmse_test = np.sqrt(mean_squared_error(y_test, predictions_test))
    r2_test = r2_score(y_test, predictions_test)
    mape_test = mean_absolute_percentage_error(y_test, predictions_test)

    print("\n", name)
    print("Train MAE:", round(mae_train, 2))
    print("Test MAE :", round(mae_test, 2))
    print("Test RMSE:", round(rmse_test, 2))
    print("Test R2  :", round(r2_test, 4))
    print("Test MAPE:", round(mape_test * 100, 2), "%")

    if mae_train / mae_test < 0.8:
        print("Potential underfitting detected (train MAE much lower than test MAE).")
    elif mae_test / mae_train > 1.5:
        print("Potential overfitting detected (test error significantly higher than train error).")

    return {
        "model": model,
        "mae": mae_test,
        "rmse": rmse_test,
        "r2": r2_test
    }


def walk_forward_validation(model, X, y, n_splits=5):
    fold = TimeSeriesSplit(n_splits=n_splits)
    metrics = []
    for train_idx, test_idx in fold.split(X):
        x_tr, x_te = X.iloc[train_idx], X.iloc[test_idx]
        y_tr, y_te = y.iloc[train_idx], y.iloc[test_idx]
        model.fit(x_tr, y_tr)
        y_pred = model.predict(x_te)
        metrics.append(mean_absolute_error(y_te, y_pred))
    return np.mean(metrics), np.std(metrics)


# ==========================================================
# 1️⃣ Linear Regression
# ==========================================================

lr = LinearRegression()

lr_results = evaluate_model(
    "Linear Regression",
    lr
)


# ==========================================================
# 2️⃣ Random Forest (Improved Baseline)
# ==========================================================

rf = RandomForestRegressor(
    n_estimators=300,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

rf_results = evaluate_model(
    "Random Forest",
    rf
)


# ==========================================================
# 3️⃣ Gradient Boosting
# ==========================================================

gb = GradientBoostingRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    random_state=42
)

gb_results = evaluate_model(
    "Gradient Boosting",
    gb
)


# ==========================================================
# 4️⃣ XGBoost Model
# ==========================================================

xgb = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42,
    n_jobs=-1
)

xgb_results = evaluate_model(
    "XGBoost",
    xgb
)


# ==========================================================
# 5️⃣ HistGradientBoosting (industry-grade regularized model)
# ==========================================================

hgb = HistGradientBoostingRegressor(
    max_iter=400,
    learning_rate=0.05,
    max_depth=7,
    min_samples_leaf=5,
    random_state=42
)

hgb_results = evaluate_model(
    "HistGradientBoosting",
    hgb
)

lgbm_results = None
catboost_results = None

if lgb is not None:
    lgbm = lgb.LGBMRegressor(
        n_estimators=400,
        learning_rate=0.03,
        num_leaves=64,
        max_depth=10,
        min_child_samples=30,
        subsample=0.85,
        colsample_bytree=0.75,
        random_state=42,
        n_jobs=-1
    )
    lgbm_results = evaluate_model("LightGBM", lgbm)

if CatBoostRegressor is not None:
    catboost = CatBoostRegressor(
        iterations=300,
        learning_rate=0.05,
        depth=6,
        loss_function="MAE",
        task_type="CPU",
        verbose=False
    )
    catboost_results = evaluate_model("CatBoost", catboost)


# ==========================================================
# Model Comparison
# ==========================================================

results = [lr_results, rf_results, gb_results, xgb_results, hgb_results]
if lgbm_results is not None:
    results.append(lgbm_results)
if catboost_results is not None:
    results.append(catboost_results)

best_model = min(results, key=lambda x: x["mae"])

print("\nBest Baseline Model:")
print(type(best_model["model"]).__name__)


# ==========================================================
# Hyperparameter Tuning - Random Forest
# ==========================================================

print("\nStarting Random Forest Hyperparameter Tuning...")

rf_param_grid = {
    "n_estimators": [200, 300],
    "max_depth": [10, 20, None],
    "min_samples_split": [2, 5],
    "min_samples_leaf": [1, 2]
}

rf_grid = GridSearchCV(
    estimator=RandomForestRegressor(random_state=42, n_jobs=-1),
    param_grid=rf_param_grid,
    cv=3,
    scoring="neg_mean_absolute_error",
    n_jobs=-1,
    verbose=1
)

rf_grid.fit(X_train, y_train)

best_rf = rf_grid.best_estimator_

print("Best Random Forest Parameters:")
print(rf_grid.best_params_)

rf_tuned_results = evaluate_model(
    "Tuned Random Forest",
    best_rf
)


# ==========================================================
# Hyperparameter Tuning - XGBoost
# ==========================================================

print("\nStarting XGBoost Hyperparameter Tuning...")

xgb_param_grid = {
    "n_estimators": [200, 300],
    "max_depth": [4, 6, 8],
    "learning_rate": [0.05, 0.1],
    "subsample": [0.8, 1]
}

xgb_grid = GridSearchCV(
    estimator=XGBRegressor(
        random_state=42,
        n_jobs=-1,
        objective="reg:squarederror"
    ),
    param_grid=xgb_param_grid,
    cv=3,
    scoring="neg_mean_absolute_error",
    n_jobs=-1,
    verbose=1
)

xgb_grid.fit(X_train, y_train)

best_xgb = xgb_grid.best_estimator_

print("Best XGBoost Parameters:")
print(xgb_grid.best_params_)

xgb_tuned_results = evaluate_model(
    "Tuned XGBoost",
    best_xgb
)


# ==========================================================
# Stacking Ensemble and Compare Tuned Models
# ==========================================================

stacking_estimators = [
    ("rf", best_rf),
    ("xgb", best_xgb)
]

if lgbm_results is not None and lgbm is not None:
    stacking_estimators.append(("lgbm", lgbm))

if catboost_results is not None and CatBoostRegressor is not None:
    stacking_estimators.append(("catboost", catboost))

stacking = StackingRegressor(
    estimators=stacking_estimators,
    final_estimator=GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=4,
        random_state=42
    ),
    passthrough=True,
    n_jobs=-1
)

stacking_results = evaluate_model("Stacking Ensemble", stacking)

# Choose best tuned model including stack
all_tuned_results = [rf_tuned_results, xgb_tuned_results, stacking_results]

best_tuned_model = min(all_tuned_results, key=lambda x: x["mae"])

print("\nBest Tuned Model:")
print(type(best_tuned_model["model"]).__name__)


# ==========================================================
# Time-Series Cross Validation for Top Candidates
# ==========================================================

print("\nRunning TimeSeriesSplit cross validation (5 folds) for top candidates...")
cv = TimeSeriesSplit(n_splits=5)
cv_targets = [
    ("RandomForest", best_rf),
    ("XGBoost", best_xgb),
    ("Stacking", stacking)
]

for name, model in cv_targets:
    scores = -cross_val_score(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring="neg_mean_absolute_error",
        n_jobs=-1
    )
    print(f"{name} CV MAE: {scores.mean():.2f} ± {scores.std():.2f}")


# Walk-forward validation (real-world sequential performance)
print("\nRunning walk-forward validation for top candidates...")
for name, model in cv_targets:
    mean_mae, std_mae = walk_forward_validation(model, X_train, y_train)
    print(f"{name} WF MAE: {mean_mae:.2f} ± {std_mae:.2f}")


# ==========================================================
# Cross Validation for XGBoost
# ==========================================================

print("\nRunning Cross Validation for XGBoost...")

scores = cross_val_score(
    best_xgb,
    X_train,
    y_train,
    cv=5,
    scoring="neg_mean_absolute_error",
    n_jobs=-1
)

print("Average CV MAE:", abs(scores.mean()))


# ==========================================================
# Feature Importance from Random Forest
# ==========================================================

os.makedirs("plots", exist_ok=True)

feature_importance = pd.Series(
    best_rf.feature_importances_,
    index=X.columns
).sort_values(ascending=False)

top_features = feature_importance.head(15)

plt.figure(figsize=(10, 7))

sns.barplot(
    x=top_features.values,
    y=top_features.index,
    hue=top_features.index,
    palette="viridis",
    legend=False
)

plt.title(
    "Top 15 Most Important Features\n(Random Forest Model)",
    fontsize=16,
    weight="bold"
)

plt.xlabel("Feature Importance Score", fontsize=12)
plt.ylabel("Feature Name", fontsize=12)

plt.tight_layout()

plt.savefig(
    "plots/random_forest_feature_importance.png",
    dpi=400,
    bbox_inches="tight"
)

plt.close()

print("Professional feature importance plot saved.")


# ==========================================================
# SHAP Explainability for XGBoost
# ==========================================================

os.makedirs("plots", exist_ok=True)

explainer = shap.TreeExplainer(xgb)
shap_values = explainer.shap_values(X_test)

plt.figure()

shap.summary_plot(
    shap_values,
    X_test,
    max_display=15,
    show=False
)

plt.title("SHAP Feature Impact on Visa Processing Time")

plt.tight_layout()

plt.savefig(
    "plots/xgboost_shap_summary.png",
    dpi=400,
    bbox_inches="tight"
)

plt.close()

print("Clean SHAP summary plot saved.")


# ==========================================================
# Save Final Best Model + Calibration Interval + Metadata
# ==========================================================

final_model = best_tuned_model["model"]

# Final evaluation metrics on test split
pred_test = final_model.predict(X_test)
residuals = y_test - pred_test
residual_lower, residual_upper = np.percentile(residuals, [5, 95])
final_mae = mean_absolute_error(y_test, pred_test)
final_rmse = np.sqrt(mean_squared_error(y_test, pred_test))
final_r2 = r2_score(y_test, pred_test)
final_mape = mean_absolute_percentage_error(y_test, pred_test)

dataset_hash = hashlib.md5(pd.util.hash_pandas_object(df, index=True).values.tobytes()).hexdigest()

print(f"Residual 90% range: [{residual_lower:.2f}, {residual_upper:.2f}]")
print(f"Final Test MAE: {final_mae:.2f}, RMSE: {final_rmse:.2f}, R2: {final_r2:.4f}, MAPE: {final_mape*100:.2f}%")

joblib.dump(final_model, "models/best_model.pkl")

# Save summary report for production verification
report = {
    "final_model": type(final_model).__name__,
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "dataset_hash": dataset_hash,
    "data_stats": {
        "data_nrows": len(df),
        "train_rows": len(X_train),
        "test_rows": len(X_test)
    },
    "final_metrics": {
        "mae": float(final_mae),
        "rmse": float(final_rmse),
        "r2": float(final_r2),
        "mape": float(final_mape)
    },
    "residual_interval_5_95": [float(residual_lower), float(residual_upper)],
    "cv_results": {
        "rf_mae": float(np.mean(np.abs(cv_targets[0][1].predict(X_test) - y_test))),
        "xgb_mae": float(np.mean(np.abs(cv_targets[1][1].predict(X_test) - y_test))),
        "stacking_mae": float(np.mean(np.abs(cv_targets[2][1].predict(X_test) - y_test)))
    }
}

with open("models/model_report.json", "w") as f:
    json.dump(report, f, indent=2)


# Save model metadata for traceability
# Convert non-serializable model params to strings for safe JSON serialization
def safe_serialize_params(params):
    serialized = {}
    for k, v in params.items():
        try:
            json.dumps(v)
            serialized[k] = v
        except TypeError:
            serialized[k] = str(v)
    return serialized

metadata = {
    "model_file": "models/best_model.pkl",
    "preprocessor_file": "models/preprocessor.pkl",
    "feature_schema_file": "models/feature_schema.json",
    "training_script": os.path.basename(__file__),
    "generated_at": datetime.utcnow().isoformat() + "Z",
    "data_hash": dataset_hash,
    "model_type": type(final_model).__name__,
    "model_params": safe_serialize_params(final_model.get_params()),
    "final_metrics": report["final_metrics"],
}

with open("models/model_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("\nFinal Best Model:", type(final_model).__name__)
print("Best model saved successfully -> models/best_model.pkl")
print("Model report saved -> models/model_report.json")
print("Model metadata saved -> models/model_metadata.json")
print("Production readiness: churned final metrics + traceability artifacts.")

# =====================================
# Additional production readiness improvements
# 1) drift report based on train vs test distribution
# 2) sample prediction capability with confidence band
# =====================================


numeric_cols_for_drift = [c for c in numeric_cols if c in df_model.columns]
train_distribution = X_train[numeric_cols_for_drift]
test_distribution = X_test[numeric_cols_for_drift]

drift_report = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "dataset_hash": dataset_hash,
    "drift_metrics": {}
}

for col in numeric_cols_for_drift:
    try:
        stat, pval = ks_2samp(train_distribution[col], test_distribution[col])
        drift_report["drift_metrics"][col] = {
            "ks_statistic": float(stat),
            "ks_pvalue": float(pval),
            "train_mean": float(train_distribution[col].mean()),
            "test_mean": float(test_distribution[col].mean())
        }
    except Exception as e:
        drift_report["drift_metrics"][col] = {"error": str(e)}

with open("models/drift_report.json", "w") as f:
    json.dump(drift_report, f, indent=2)

print("Drift report saved -> models/drift_report.json")

# Conformal residual-based interval helper (applies to predictions after deployment)
residual_q05 = np.quantile(residuals, 0.05)
residual_q95 = np.quantile(residuals, 0.95)


def predict_with_uncertainty(X_new):
    y_pred = final_model.predict(X_new)
    return {
        "prediction": y_pred,
        "lower_90": y_pred + residual_q05,
        "upper_90": y_pred + residual_q95,
        "residual_interval": [float(residual_q05), float(residual_q95)]
    }

print("Prediction interval helper ready (lower/upper 90%).")
