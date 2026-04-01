import pandas as pd
import os


# ==========================================================
# CONFIGURATION
# ==========================================================

RAW_DATA_PATH = "data/processed/2013_2025_raw_dataset.csv"
OUTPUT_DIR = "data/processed"
CLEAN_DATA_PATH = os.path.join(OUTPUT_DIR, "cleaned_dataset.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Starting Data Cleaning Pipeline...\n")


# ==========================================================
# STEP 1: LOAD DATA
# ==========================================================

print("Loading raw dataset...")

df = pd.read_csv(
    RAW_DATA_PATH,
    low_memory=False
)

print("Initial Dataset Shape:", df.shape)
print("Columns:", list(df.columns))


# ==========================================================
# STEP 2: STANDARDIZE COLUMN NAMES
# ==========================================================

print("\nStandardizing column names...")

column_mapping = {
    "caseNumber": "case_id",
    "submitDate": "application_date",
    "statusDate": "decision_date",
    "status": "case_status",
    "consulate": "processing_office"
}

df.rename(columns=column_mapping, inplace=True)

required_columns = [
    "case_id",
    "application_date",
    "decision_date",
    "processing_office",
    "region"
]

missing_cols = [c for c in required_columns if c not in df.columns]

if missing_cols:
    raise ValueError(f"Missing required columns: {missing_cols}")


# ==========================================================
# STEP 3: CONVERT DATE COLUMNS
# ==========================================================

print("\nConverting date columns...")

df["application_date"] = pd.to_datetime(
    df["application_date"],
    errors="coerce",
    format="mixed"
)

df["decision_date"] = pd.to_datetime(
    df["decision_date"],
    errors="coerce",
    format="mixed"
)


# ==========================================================
# STEP 4: REMOVE INVALID RECORDS
# ==========================================================

print("\nRemoving rows with invalid critical values...")

before_rows = df.shape[0]

df = df.dropna(
    subset=["case_id", "application_date", "decision_date"]
)

after_rows = df.shape[0]

print(f"Removed {before_rows - after_rows} invalid rows")


# ==========================================================
# STEP 5: CREATE TARGET VARIABLE
# ==========================================================

print("\nCreating target variable: processing_time_days")

df["processing_time_days"] = (
    df["decision_date"] - df["application_date"]
).dt.days

df = df[df["processing_time_days"] >= 0]

df["processing_time_days"] = df["processing_time_days"].astype(int)

print("Target variable created successfully")


# ==========================================================
# STEP 6: HANDLE MISSING CATEGORICAL VALUES + NORMALIZATION
# ==========================================================

print("\nHandling missing categorical values and normalization...")

categorical_columns = [
    "region",
    "processing_office"
]

for col in categorical_columns:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().replace(["", "nan", "None", "NoneType"], "Unknown")
        df[col] = df[col].fillna("Unknown")
        df[col] = df[col].str.upper()

# Remove leakage features that are not allowed in production prediction
leak_cols = ["case_status", "Issued", "AP", "Ready", "Refused", "InTransit", "Transfer", "NVC", "Refused221g"]
for col in leak_cols:
    if col in df.columns:
        df = df.drop(columns=[col])

# Derive additional stable features from dates
print("\nCreating time-derived features...")

if "application_date" in df.columns:
    df["application_year"] = df["application_date"].dt.year
    df["application_month"] = df["application_date"].dt.month
    df["application_quarter"] = df["application_date"].dt.to_period("Q").dt.quarter
    df["application_week"] = df["application_date"].dt.isocalendar().week

if "decision_date" in df.columns:
    df["decision_year"] = df["decision_date"].dt.year
    df["decision_month"] = df["decision_date"].dt.month
    df["decision_quarter"] = df["decision_date"].dt.to_period("Q").dt.quarter

# Replace unknown region office with 'UNKNOWN'
if "region" in df.columns:
    df.loc[df["region"].isin(["", "UNKNOWN", "N/A"]), "region"] = "UNKNOWN"

if "processing_office" in df.columns:
    df.loc[df["processing_office"].isin(["", "UNKNOWN", "N/A"]), "processing_office"] = "UNKNOWN"


# ==========================================================
# STEP 7: HANDLE HIGH-MISSING + QUALITY CHECKS
# ==========================================================

print("\nFixing problematic columns and quality checks...")

columns_to_drop = ["potentialAP", "2nlDate"]

df = df.drop(columns=[c for c in columns_to_drop if c in df.columns])

# Remove records with invalid stats after feature extraction
print("Removing rows with numeric anomalies...")

if "processing_time_days" in df.columns:
    df = df[(df["processing_time_days"] >= 0) & (df["processing_time_days"] <= 2000)]

# Strong outlier handling grouped by region/office
if set(["region", "processing_office", "processing_time_days"]).issubset(df.columns):
    grouped = df.groupby(["region", "processing_office"])["processing_time_days"]
    q1 = grouped.transform(lambda x: x.quantile(0.05))
    q3 = grouped.transform(lambda x: x.quantile(0.95))
    valid = (df["processing_time_days"] >= q1) & (df["processing_time_days"] <= q3)
    df = df[valid]

print("Problematic columns fixed")


# ==========================================================
# STEP 8: REMOVE DUPLICATES + CONSISTENCY
# ==========================================================

print("\nRemoving duplicate cases and enforcing consistency...")

df = df.sort_values("decision_date")

before_dup = df.shape[0]

df = df.drop_duplicates(
    subset="case_id",
    keep="last"
)

after_dup = df.shape[0]

print(f"Removed {before_dup - after_dup} duplicate cases")

# Remove exact duplicate row entries after processing
before_dedup = df.shape[0]
df = df.drop_duplicates()
after_dedup = df.shape[0]
print(f"Removed {before_dedup - after_dedup} exact duplicate rows")


# ==========================================================
# STEP 9: ADD STATIC FEATURES
# ==========================================================

print("\nAdding visa type feature...")

df["visa_type"] = "DV_Lottery"


# ==========================================================
# STEP 10: DATA VALIDATION CHECKS
# ==========================================================

print("\nRunning dataset validation...")

print("\nDataset Info:")
print(df.info())

print("\nProcessing Time Statistics:")
print(df["processing_time_days"].describe())

print("\nMissing Values:")
print(df.isnull().sum())


# ==========================================================
# STEP 11: SAVE CLEAN DATASET
# ==========================================================

df["case_id"] = df["case_id"].astype(str)

# We intentionally omit case status-derived signals to avoid data leakage.
status_cols = [
    "Issued",
    "AP",
    "Ready",
    "Refused",
    "InTransit",
    "Transfer",
    "NVC",
    "Refused221g"
]

for col in status_cols:
    if col in df.columns:
        df[col] = df[col].fillna(0).astype(int)

# Remove extreme outliers to improve model generalization
q_low = df["processing_time_days"].quantile(0.01)
q_high = df["processing_time_days"].quantile(0.99)
df = df[(df["processing_time_days"] >= q_low) & (df["processing_time_days"] <= q_high)]

print("\nSaving cleaned dataset...")

df.to_csv(CLEAN_DATA_PATH, index=False)

print("Clean dataset saved successfully")

print("\nFinal Dataset Shape:", df.shape)

print("\nData Cleaning Pipeline Completed")
