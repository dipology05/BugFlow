
import pandas as pd

# Load the existing dataset
df = pd.read_csv("bugs_dataset.csv")

print("\n--- DATASET SHAPE ---")
print("Rows and columns:", df.shape)

print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

print("\n--- FIRST 5 ROWS ---")
print(df.head().to_string())

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- SEVERITY DISTRIBUTION ---")
print(df["Severity Label"].value_counts(dropna=False))

print("\n--- RESOLUTION STATUS ---")
print(df["Resolution Status"].value_counts(dropna=False))

print("\n--- DUPLICATE ROWS ---")
print(df.duplicated().sum())
