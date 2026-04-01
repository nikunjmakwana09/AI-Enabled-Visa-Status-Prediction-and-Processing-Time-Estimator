# AI-Enabled Visa Status Prediction & Processing Time Estimator

**Milestone 2 — Exploratory Data Analysis & Feature Engineering**

### Objective

The goal of Milestone 2 is to analyze patterns in visa processing data and engineer features that improve predictive modeling performance.

This stage focuses on:

* identifying processing time trends
* analyzing regional and operational workload patterns
* creating new temporal and operational features
* ensuring feature design aligns with real-world prediction constraints (no data leakage)

The engineered dataset will be used for **machine learning model training in Milestone 3**.

---

## Dataset

Input dataset generated in **Milestone 1**:

```
data/processed/cleaned_dataset.csv
```

Dataset summary:

| Metric             | Value                |
| ------------------ | -------------------- |
| Records            | 50,135               |
| Regions            | 5 global regions     |
| Processing Offices | 130+                 |
| Target Variable    | processing_time_days |

---

## Exploratory Data Analysis (EDA)

EDA was performed using **Matplotlib** and **Seaborn**.

Key analyses included:

### Temporal Trends

* Average processing time by fiscal year
* Year-over-year processing time changes

Outputs:

```
plots/year_trend.png
plots/yearly_percentage_change.png
```

### Distribution Analysis

Understanding the spread of visa processing durations.

```
plots/processing_time_distribution.png
```

### Regional Analysis

Comparison of processing times across global regions.

```
plots/processing_time_by_region.png
```

### Processing Office Analysis

Comparison of processing time distributions across the **top 10 consulates**.

```
plots/processing_time_top_offices.png
```

### Workload Analysis

Relationship between office workload and processing time.

```
plots/workload_vs_time.png
```

---

## Feature Engineering

Several features were created to capture seasonal trends and operational workload.

### Temporal Features

```
application_month
application_quarter
application_year
```

These help capture seasonal processing patterns.

### Workload Feature

```
office_volume
```

Represents the number of applications handled by each processing office.

### Rolling Trend Features

office_rolling_30_mean  
office_rolling_30_std  
region_rolling_30_mean  
region_rolling_30_std

These features capture short-term historical trends and variability in processing time using rolling window calculations.

They provide strong predictive signals for recent workload behavior.

### Trend Change Feature

office_mom_diff

Represents month-over-month change in processing time at the office level.

This helps capture dynamic operational shifts and backlog changes.

### Aggregate Features

```
region_avg_time
office_avg_time
```

Historical processing performance by region and office.

Note: These features are used as baseline indicators and are carefully designed to support modeling. In production systems, they should be computed using past data only to avoid leakage.

### Advanced Features

```
season_index
office_pressure
```
• season_index captures peak application seasons (Jan, Feb, Dec)
• office_pressure approximates workload intensity using:
office_pressure = office_volume / office_avg_time

These features help model seasonality and operational stress.

---

### Data Leakage Prevention

• Removed case_status and all post-decision signals
• Ensured all engineered features are based on pre-decision or historical data
• Maintained alignment with real-world prediction scenarios

## Correlation Analysis

A correlation matrix was generated to identify relationships between numerical features and processing time.

Outputs:

```
outputs/correlation_matrix.csv
plots/correlation_matrix.png
```
This helps in:
• identifying strong predictors
• removing redundant features
• improving model efficiency

---

## Engineered Dataset

The final dataset generated in this milestone:

```
data/processed/engineered_dataset.csv
```

This dataset contains original cleaned features along with newly engineered features.

---

## Project Structure

```
notebooks/scripts/
 └── eda_feature_engineering.py

plots/
outputs/

data/processed/
 ├── cleaned_dataset.csv
 └── engineered_dataset.csv
```

---

## Outcome

✔ Exploratory data analysis completed
✔ Temporal and operational patterns identified
✔ Advanced rolling and trend-based features engineered
✔ Data leakage risks minimized
✔ Dataset prepared for machine learning

The dataset is now ready for **model training in Milestone 3**.
