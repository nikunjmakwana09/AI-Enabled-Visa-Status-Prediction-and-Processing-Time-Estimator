import pandas as pd
import glob
import os
import re


# ==========================================================
# Combine CEAC datasets from multiple fiscal years
# ==========================================================

files = glob.glob("data/raw/FY*-ceac-*.csv")

dfs = []

for file in files:
    df = pd.read_csv(file, low_memory=False)

    # Extract filename only
    filename = os.path.basename(file)

    # Extract fiscal year using regex
    match = re.search(r"FY(\d{4})", filename)

    if match:
        fy = int(match.group(1))
    else:
        raise ValueError(f"Fiscal year not found in filename: {filename}")

    df["fiscal_year"] = fy
    dfs.append(df)


# ==========================================================
# Concatenate all dataframes into one
# ==========================================================

dv_df = pd.concat(dfs, ignore_index=True)


# ==========================================================
# Save combined dataset
# ==========================================================

output_path = "data/processed/2013_2025_raw_dataset.csv"
dv_df.to_csv(output_path, index=False)

print("Combined dataset saved.")
