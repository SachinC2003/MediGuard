# generate_data.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_excel("🧠 1. Healthcare dataset.xlsx", sheet_name="🧠 1. Structured Health Records")

# Split BP into systolic & diastolic
df[['Systolic', 'Diastolic']] = df['Blood Pressure (mmHg)'].str.split('/', expand=True).astype(int)

# Encode categorical columns
label_encoders = {}
for col in ['Gender', 'Medical History', 'Family History']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le

# Encode target (Diagnosis)
target_le = LabelEncoder()
df['Diagnosis'] = target_le.fit_transform(df['Diagnosis (ICD-10)'])

# Select features
X = df[['Age', 'Gender', 'Weight (kg)', 'Height (cm)', 'Medical History', 
        'Family History', 'Systolic', 'Diastolic',
        'Blood Glucose (mg/dL)', 'Cholesterol (mg/dL)']].values
y = df['Diagnosis'].values

# Split into N clients (example: 3)
splits = np.array_split(np.random.permutation(len(X)), 3)

for i, idx in enumerate(splits, start=1):
    np.save(f"data/client{i}_X.npy", X[idx])
    np.save(f"data/client{i}_y.npy", y[idx])

print("✅ Data generated for all clients!")
