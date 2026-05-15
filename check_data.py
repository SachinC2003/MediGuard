import pandas as pd

# Check megaProject dataset
df = pd.read_csv("megaProject/Diseases_and_Symptoms_dataset.csv")
print(f"Dataset shape: {df.shape}")
print(f"Number of diseases: {df['diseases'].nunique()}")
print(f"Disease classes:\n{sorted(df['diseases'].unique())}")
