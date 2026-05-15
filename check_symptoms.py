import pandas as pd

# Load dataset
df = pd.read_csv('megaProject/Diseases_and_Symptoms_dataset.csv')
symptom_columns = df.columns[1:]  # Skip diseases column

print(f"Dataset has {len(symptom_columns)} symptoms")
print("\nFirst 10 symptoms in dataset:")
for i in range(10):
    print(f"{i}: {symptom_columns[i]}")

print("\nLast 10 symptoms in dataset:")
for i in range(len(symptom_columns)-10, len(symptom_columns)):
    print(f"{i}: {symptom_columns[i]}")

# Check specific symptoms the user mentioned
user_symptoms = ["cough", "fever", "shortness of breath"]
print(f"\nChecking user symptoms: {user_symptoms}")
for symptom in user_symptoms:
    if symptom in symptom_columns:
        idx = symptom_columns.get_loc(symptom)
        print(f"'{symptom}' found at index {idx}")
    else:
        print(f"'{symptom}' NOT FOUND in dataset!")

# Check pneumonia symptoms
print("\nTop pneumonia symptoms from earlier analysis:")
pneumonia_symptoms = ["vomiting", "cough", "nasal congestion", "weakness", "sore throat"]
for symptom in pneumonia_symptoms:
    if symptom in symptom_columns:
        idx = symptom_columns.get_loc(symptom)
        print(f"'{symptom}' at index {idx}")
    else:
        print(f"'{symptom}' NOT FOUND!")