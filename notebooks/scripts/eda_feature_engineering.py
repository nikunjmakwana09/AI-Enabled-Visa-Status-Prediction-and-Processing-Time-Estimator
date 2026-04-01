import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ==========================================================
# CONFIG
# ==========================================================

INPUT_PATH = "data/processed/cleaned_dataset.csv"
OUTPUT_DATA = "data/processed/engineered_dataset.csv"

PLOTS_DIR = "plots"
OUTPUT_DIR = "outputs"

os.makedirs(PLOTS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.style.use("seaborn-v0_8")
sns.set_context("talk")


# ==========================================================
# LOAD DATA
# ==========================================================

print("Loading cleaned dataset...")

df = pd.read_csv(
    INPUT_PATH,
    parse_dates=["application_date", "decision_date"]
)

df["case_id"] = df["case_id"].astype(str)

# Project standards: no leakage from final status
if "case_status" in df.columns:
    df = df.drop(columns=["case_status"])

# normalize categorical columns
for c in ["region", "processing_office", "visa_type"]:
    if c in df.columns:
        df[c] = df[c].astype(str).str.strip().str.upper().replace({"": "UNKNOWN", "N/A": "UNKNOWN", "NONE": "UNKNOWN"})

print("Dataset loaded")
print("Shape:", df.shape)


# ==========================================================
# BASIC EDA
# ==========================================================

print("Generating EDA plots...")

# Year Trend Analysis

plt.figure(figsize=(9, 6))
df.groupby("fiscal_year")["processing_time_days"].mean().plot(marker="o")
plt.title("Average Processing Time by Fiscal Year", fontsize=14)
plt.ylabel("Average Processing Time (Days)")
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/year_trend.png", dpi=300)
plt.close()

# Year-over-Year % Change in Processing Time

year_avg = df.groupby("fiscal_year")["processing_time_days"].mean()
year_change = year_avg.pct_change() * 100

plt.figure(figsize=(9, 6))
year_change.plot(marker="o")
plt.title("Year-over-Year % Change in Processing Time", fontsize=14)
plt.xlabel("Fiscal Year")
plt.ylabel("Percentage Change")
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/yearly_percentage_change.png", dpi=300)
plt.close()

# Processing time distribution

plt.figure(figsize=(9, 6))
sns.histplot(df["processing_time_days"], bins=30, kde=True, color="teal")
plt.title("Processing Time Distribution", fontsize=14)
plt.xlabel("Processing Time (Days)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/processing_time_distribution.png", dpi=300)
plt.close()

# Processing time by region

plt.figure(figsize=(10, 6))
sns.boxplot(x="region", y="processing_time_days", data=df)
plt.title("Processing Time by Region", fontsize=14)
plt.xlabel("Region")
plt.ylabel("Processing Time (Days)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/processing_time_by_region.png", dpi=300)
plt.close()

# Processing Time by Top 10 Processing Offices

top_offices = df["processing_office"].value_counts().nlargest(10).index

plt.figure(figsize=(14, 6))

sns.boxplot(
    x="processing_office",
    y="processing_time_days",
    data=df[df["processing_office"].isin(top_offices)]
)

plt.xticks(rotation=60)
plt.title("Processing Time - Top 10 Processing Offices", fontsize=14)
plt.tight_layout()
plt.savefig("plots/processing_time_top_offices.png", dpi=300)
plt.close()


# ==========================================================
# FEATURE ENGINEERING
# ==========================================================

print("Creating temporal features...")

# Month feature
df["application_month"] = df["application_date"].dt.month

# Quarter feature
df["application_quarter"] = df["application_date"].dt.quarter

# Year feature
df["application_year"] = df["application_date"].dt.year

# Scatter plot for month vs processing time

plt.figure(figsize=(8, 6))
sns.scatterplot(
    x="application_month",
    y="processing_time_days",
    data=df
)
plt.title("Processing Time vs Application Month")
plt.tight_layout()
plt.savefig("plots/month_vs_processing.png", dpi=300)
plt.close()


# ==========================================================
# WORKLOAD FEATURES
# ==========================================================

print("Creating workload features...")

# Office workload
office_counts = df["processing_office"].value_counts()

df["office_volume"] = df["processing_office"].map(office_counts)

# Time-based features for rolling trends (industry-grade predictive signal)
print("Creating rolling features for office and region trend detection...")

df = df.sort_values("application_date")

df["application_year_month"] = df["application_date"].dt.to_period("M").dt.to_timestamp()

for group_col, suffix in [("processing_office", "office"), ("region", "region")]:
    df[f"{suffix}_rolling_30_mean"] = (
        df.groupby(group_col)["processing_time_days"]
          .transform(lambda x: x.rolling(window=30, min_periods=5).mean())
    )
    df[f"{suffix}_rolling_30_std"] = (
        df.groupby(group_col)["processing_time_days"]
          .transform(lambda x: x.rolling(window=30, min_periods=5).std().fillna(0))
    )

# Add office-level historical month-over-month trend (delta) as a signal for pressure
monthly_speed = df.groupby(["processing_office", "application_year", "application_month"])["processing_time_days"].mean().rename("office_monthly_mean").reset_index()
monthly_speed["office_mom_diff"] = monthly_speed.groupby("processing_office")["office_monthly_mean"].diff().fillna(0)

# map back to main frame
monthly_speed["year_month"] = pd.to_datetime(monthly_speed["application_year"].astype(str) + "-" + monthly_speed["application_month"].astype(str).str.zfill(2))
DF_MONTHLY = monthly_speed.set_index(["processing_office", "year_month"])['office_mom_diff']

# Ideally use .loc with column, avoid SettingWithCopy warnings
transform_idx = pd.MultiIndex.from_arrays([df["processing_office"], df["application_date"].dt.to_period("M").dt.to_timestamp()])
df["office_mom_diff"] = DF_MONTHLY.reindex(transform_idx).values

df["office_mom_diff"] = df["office_mom_diff"].fillna(0)

# Fill rolling missing values from group mean or global fallback to avoid leakage
if "office_rolling_30_mean" in df.columns:
    office_mean = df["office_rolling_30_mean"].mean()
    df["office_rolling_30_mean"] = df["office_rolling_30_mean"].fillna(office_mean)

if "region_rolling_30_mean" in df.columns:
    region_mean = df["region_rolling_30_mean"].mean()
    df["region_rolling_30_mean"] = df["region_rolling_30_mean"].fillna(region_mean)

# Workload vs Processing Time

office_stats = df.groupby("processing_office").agg({
    "processing_time_days": "mean",
    "case_id": "count"
}).rename(columns={"case_id": "volume"})

plt.figure(figsize=(9, 6))
plt.scatter(
    office_stats["volume"],
    office_stats["processing_time_days"],
    alpha=0.7
)

plt.title("Workload vs Processing Time", fontsize=14)
plt.xlabel("Office Volume")
plt.ylabel("Average Processing Time (Days)")
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/workload_vs_time.png", dpi=300)
plt.close()


# ==========================================================
# AGGREGATE FEATURES (SAFE)
# ==========================================================

print("Creating regional processing trends...")

region_avg = df.groupby("region")["processing_time_days"].mean()

df["region_avg_time"] = df["region"].map(region_avg)

office_avg = df.groupby("processing_office")["processing_time_days"].mean()

df["office_avg_time"] = df["processing_office"].map(office_avg)


# ==========================================================
# ADVANCED FEATURES
# ==========================================================

print("Creating advanced seasonal and workload features...")

# Feature 1: Seasonal index
df["season_index"] = df["application_month"].apply(
    lambda x: 1 if x in [1, 2, 12] else 0
)

# Feature 2: Office pressure
df["office_pressure"] = df["office_volume"] / df["office_avg_time"]


# ==========================================================
# CORRELATION ANALYSIS
# ==========================================================

print("Generating correlation matrix...")

numeric_df = df.select_dtypes(include=["int64", "float64"])

corr = numeric_df.corr()

corr.to_csv(f"{OUTPUT_DIR}/correlation_matrix.csv")

plt.figure(figsize=(12, 10))
sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    annot_kws={"size": 10},
    linewidths=0.5
)
plt.title("Correlation Matrix", fontsize=16)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/correlation_matrix.png", dpi=300)
plt.close()


# ==========================================================
# FINAL DATASET VALIDATION
# ==========================================================

print("\nEngineered Dataset Summary")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())


# ==========================================================
# SAVE ENGINEERED DATASET
# ==========================================================

df.to_csv(OUTPUT_DATA, index=False)

print("\nFeature engineering completed successfully")
print("Saved to:", OUTPUT_DATA)
