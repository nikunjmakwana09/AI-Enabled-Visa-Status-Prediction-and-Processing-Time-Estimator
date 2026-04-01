# AI-Enabled Visa Status Prediction & Processing Time Estimator

**Milestone 1 — Data Collection & Preprocessing**

### Objective

The goal of Milestone 1 is to construct a clean and structured dataset suitable for machine learning.
This stage focuses on collecting historical visa application data, cleaning inconsistencies, and generating the **target variable representing visa processing time**.

---

## Dataset Overview

The dataset is based on publicly available **Diversity Visa (DV Lottery)** records from the Consular Electronic Application Center (CEAC).

**Coverage**

* Fiscal Years: 2013 – 2025
* Global Regions: Africa, Asia, Europe, Oceania, South America
* Processing Offices: 130+ U.S. consulates worldwide

These records represent real visa processing activity across multiple regions.

---

## Data Preprocessing Pipeline

Two scripts implement the preprocessing workflow.

### 1. Dataset Combination (`combine_datasets.py`)

Steps:

* Load CEAC datasets from multiple fiscal years
* Extract fiscal year from file names
* Append fiscal year as a new feature
* Merge datasets into a single dataframe

Output:

```
data/processed/2013_2025_raw_dataset.csv
```

---

### 2. Data Cleaning (`prepare_dataset.py`)

The cleaning pipeline performs the following steps:

**Column Standardization**

Renames raw dataset fields to consistent names.

Example:

```
caseNumber → case_id
submitDate → application_date
statusDate → decision_date
consulate → processing_office
```

**Date Conversion**

Application and decision dates are converted into datetime format.

**Invalid Record Removal**

Records missing critical information are removed:

* application_date
* decision_date
* case_id

**Target Variable Generation**

Processing time is calculated as:

```
processing_time_days = decision_date - application_date
```

Only valid (non-negative) values are retained.

**Data Leakage Prevention**

To ensure real-world prediction capability, post-decision features are removed, including:
case_status  
Issued, AP, Ready, Refused, InTransit, Transfer, NVC, Refused221g  

These features are only available after visa processing and including them would lead to unrealistic (leakage-based) predictions.

**Missing Value Handling**

Categorical variables are filled with `"Unknown"` where necessary.

**Categorical Normalization**

• Trim spaces
• Convert to uppercase
• Replace invalid values ("", nan, None) with "UNKNOWN"

**High Missing Column Handling**

Columns with extremely high missing rates are removed:

```
potentialAP
2nlDate
```

**Time-Based Feature Engineering**

Additional features are derived from application date:
application_year  
application_month  
application_quarter  
application_week  

These features capture temporal trends in visa processing.

**Outlier Handling**

To improve model generalization:
• Group-wise filtering (5th—95th percentile) based on region and processing office
• Global filtering (1st—99th percentile)

This removes extreme anomalies while preserving realistic patterns.

**Duplicate Removal**

Duplicate case records are removed using `case_id`, keeping the latest decision entry.

**Static Feature Addition**

A feature identifying visa type is added:

```
visa_type = DV_Lottery
```

---

## Final Dataset Summary

After preprocessing:

| Metric          | Value                |
| --------------- | -------------------- |
| Total records   | 50,135               |
| Total features  | Cleaned & engineered |
| Missing values  | None                 |
| Target variable | processing_time_days |

Processing time ranges between approximately **330 and 730 days**.

---

## Project Structure

```
data/
 ├── raw/
 │   └── FY2013–FY2025 CEAC datasets
 │
 └── processed/
     ├── 2013_2025_raw_dataset.csv
     └── cleaned_dataset.csv

notebooks/scripts/
 ├── combine_datasets.py
 └── prepare_dataset.py
```

---

## Output

✔ Cleaned and validated dataset
✔ No missing values
✔ No data leakage
✔ Ready for machine learning

The dataset is now ready for **EDA & Feature Engineering in Milestone 2**.
