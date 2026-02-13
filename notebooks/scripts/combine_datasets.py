import pandas as pd
import glob
import os
import re

# Get all FY CSV files
files = glob.glob("data/raw/FY*-ceac-*.csv")

dfs = []

for file in files:
    df = pd.read_csv(file)

    # Extract filename only (Windows-safe)
    filename = os.path.basename(file)

    # Extract fiscal year using regex
    match = re.search(r"FY(\d{4})", filename)

    if match:
        fy = int(match.group(1))
    else:
        raise ValueError(f"Fiscal year not found in filename: {filename}")

    df["fiscal_year"] = fy
    dfs.append(df)

# Combine all fiscal years
dv_df = pd.concat(dfs, ignore_index=True)

# Save combined dataset
output_path = "data/processed/2013_2025_raw_dataset.csv"
dv_df.to_csv(output_path, index=False)
