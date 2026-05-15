import pandas as pd

# Get the exact symptom names from dataset
df = pd.read_csv('megaProject/Diseases_and_Symptoms_dataset.csv')
symptom_columns = list(df.columns[1:])  # Skip diseases column

print('EXACT symptom list from dataset (copy this to frontend):')
print('const ALL_SYMPTOMS: string[] = [')
for i, symptom in enumerate(symptom_columns):
    if i < len(symptom_columns) - 1:
        print(f'  "{symptom}",')
    else:
        print(f'  "{symptom}"')
print('];')

print(f'\nTotal symptoms: {len(symptom_columns)}')

# Check specific symptoms
print('\nChecking user symptoms:')
user_symptoms = ["cough", "fever", "shortness of breath"]
for symptom in user_symptoms:
    if symptom in symptom_columns:
        idx = symptom_columns.index(symptom)
        print(f"'{symptom}' is at index {idx}")
    else:
        print(f"'{symptom}' NOT FOUND!")