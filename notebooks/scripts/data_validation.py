import pandas as pd

df = pd.read_csv("data/processed/final_dataset.csv",)

# Check the first few rows
print(df.head())

# Check the last few rows
print(df.tail())

# Check the structure of the dataset
print(df.info())

# Check the index and columns of the DataFrame
print(df.axes)

# Check columns
print(df.columns)

# Check the shape of the dataset
print(df.shape)

# Check data types
print(df.dtypes)

# Check for missing values
print(df.isnull().sum())

# Check for negative processing times
invalid_dates = df[df["processing_time_days"] < 0]
print("Invalid date records:", len(invalid_dates))

# Summary statistics of processing times
print(df["processing_time_days"].describe())

# Check duplicate rows (FULL ROW)
duplicate_rows = df.duplicated().sum()
print(
    "\nRows with identical feature vectors (expected after encoding):",
    duplicate_rows
)

# Check encoded columns (0/1)
encoded_cols = [c for c in df.columns if "_" in c]

invalid_encoded = {
    col: df[col].unique()
    for col in encoded_cols
    if not set(df[col].unique()).issubset({0, 1})
}
