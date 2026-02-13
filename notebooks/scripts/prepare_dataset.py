import pandas as pd

# -----------------------------------
# Load raw combined dataset
# -----------------------------------
df = pd.read_csv("data/processed/2013_2025_raw_dataset.csv")

# -----------------------------------
# 1. Standardize column names
# -----------------------------------
column_mapping = {
    "caseNumber": "case_id",
    "submitDate": "application_date",
    "statusDate": "decision_date",
    "status": "case_status",
    "consulate": "processing_office"
}

df.rename(columns=column_mapping, inplace=True)

# -----------------------------------
# 2. Convert date columns
# -----------------------------------
df["application_date"] = pd.to_datetime(df["application_date"], errors="coerce")
df["decision_date"] = pd.to_datetime(df["decision_date"], errors="coerce")

# -----------------------------------
# 3. Create target variable
# -----------------------------------
df["processing_time_days"] = (df["decision_date"] - df["application_date"]).dt.days
df = df[df["processing_time_days"] >= 0]
df["processing_time_days"] = df["processing_time_days"].astype(int)

# -----------------------------------
# 4. Drop rows with missing critical values
# -----------------------------------
# Drop invalid dates
df.dropna(
    subset=["application_date", "decision_date", "case_id"],
    inplace=True
)

# Fill categorical columns (if needed)
df["region"].fillna("Unknown", inplace=True)
df["processing_office"].fillna("Unknown", inplace=True)
df["case_status"].fillna("Unknown", inplace=True)

# -----------------------------------
# 5. Remove duplicate cases (keep latest decision)
# -----------------------------------
df.sort_values(by="decision_date", inplace=True)
df = df.drop_duplicates(subset=["case_id"], keep="last")

# -----------------------------------
# 6. Keep only important columns
# -----------------------------------
base_columns = [
    "region",
    "processing_office",
    "case_status",
    "fiscal_year",
    "processing_time_days"
]

df = df[base_columns]

# Add visa type column (since this dataset is only for DV Lottery)
df["visa_type"] = "DV_Lottery"

# -----------------------------------
# 7. ONE-HOT ENCODING
# -----------------------------------
categorical_cols = [
    "region",
    "processing_office",
    "case_status",
    "visa_type"
]


df_final = pd.get_dummies(
    df,
    columns=categorical_cols,
    drop_first=False
)

# -----------------------------------
# 8. Save FINAL DATASET
# -----------------------------------
df_final.to_csv(
    "data/processed/final_dataset.csv",
    index=False
)
