AI-Enabled Visa Status Prediction & Processing Time Estimator

Milestone 1 – Data Collection & Preprocessing

📌 Objective
The objective of Milestone 1 is to collect historical visa data, clean and preprocess the dataset, generate the target variable (processing time in days), and prepare a structured dataset suitable for machine learning modeling.

📂 Dataset Overview
Data Source
The dataset used in this milestone is based on publicly available Diversity Visa (DV Lottery) application data (Fiscal Years 2013–2025).

The Diversity Visa program represents immigrant visa applications processed globally, making it suitable for building a generalized visa processing time estimation system.

🌍 Geographic Coverage
The dataset includes applications from multiple global regions:
• Africa (AF)
• Asia (AS)
• Europe (EU)
• Oceania (OC)
• South America (SA)

A total of 133 U.S. consulates (processing offices) are represented in the dataset.

    Note: Country-level information is inferred through consulate and regional indicators, as the dataset does not explicitly provide a country column.

🧹 Data Preprocessing Steps
The following preprocessing steps were performed:
1️⃣ Column Standardization
• Renamed raw columns to consistent and meaningful names.
• Standardized date formats.

2️⃣ Missing Value Handling
• Removed records with missing application or decision dates.
• Ensured no missing values remain in the final dataset.

3️⃣ Target Variable Generation
• A new column processing_time_days was created:
processing_time_days = decision_date - application_date

This column represents the number of days taken for visa processing and serves as the primary prediction target.

4️⃣ Duplicate Handling
• Duplicate case records were removed.
• After one-hot encoding, identical feature rows were retained as they represent valid independent cases.

5️⃣ One-Hot Encoding
Categorical features were converted into numerical format using one-hot encoding:
• region
• processing_office (consulate)
• case_status
This ensures compatibility with machine learning algorithms.

📊 Final Dataset Characteristics
• Total Records: 52,187
• Total Features (after encoding): 148
• No missing values
• All features are numeric (bool or int)
• Target variable: processing_time_days

The final encoded dataset is:
data/processed/final_dataset.csv

🏗️ Project Structure (Milestone 1)
data/processed/
 ├── 2013_2025_raw_dataset.csv
 └── final_dataset.csv

data/raw/
 ├── FY2013-ceac-current.csv
 ├── FY2014-ceac-current.csv
 ├── FY2015-ceac-current.csv
 ├── FY2016-ceac-current.csv
 ├── FY2018-ceac-current.csv
 ├── FY2019-ceac-current.csv
 ├── FY2020-ceac-current.csv
 ├── FY2021-ceac-current.csv
 ├── FY2022-ceac-current.csv
 ├── FY2023-ceac-2023-06-24.csv
 ├── FY2024-ceac-2024-10-01.csv
 └── FY2025-ceac-2025-10-01.csv

notebooks/scripts/
 ├── combine_datasets.py
 ├── prepare_dataset.py
 └── data_validation.py

🔮 Future Scope
• Integration of additional visa categories (Student, Work, Tourist, etc.)
• Incorporation of explicit country-level data
• Model training and evaluation (Milestone 2+)
• Deployment-ready prediction system

🎯 End of Milestone 1