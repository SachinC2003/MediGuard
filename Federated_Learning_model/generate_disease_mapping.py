"""
Utility to generate correct disease mapping from the dataset
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pickle
import json

# Load dataset
df = pd.read_csv("Diseases_and_Symptoms_dataset.csv")

# Create and fit label encoder
le = LabelEncoder()
y_encoded = le.fit_transform(df['diseases'])

# Get disease names
disease_names = list(le.classes_)

print(f"Total diseases: {len(disease_names)}")
print(f"Disease names: {disease_names}")

# Save label encoder for backend
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

# Save disease names as JSON
with open("disease_names.json", "w") as f:
    json.dump(disease_names, f, indent=2)

print("\n✅ Saved label_encoder.pkl and disease_names.json")
