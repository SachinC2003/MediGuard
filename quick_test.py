import requests
import json

# Load disease names
with open('flask-backend/disease_names.json', 'r') as f:
    DISEASES = json.load(f)

def quick_test(symptoms_dict, test_name):
    features = [0] * 230
    for symptom, index in symptoms_dict.items():
        features[index] = 1

    try:
        response = requests.post('http://localhost:5000/predict',
                               json={'features': features, 'return_top_k': 3},
                               headers={'Content-Type': 'application/json'},
                               timeout=5)

        if response.status_code == 200:
            data = response.json()
            print(f'{test_name}:')
            print(f'  Primary: {data["disease"]} ({data["confidence"]*100:.1f}%)')
            if 'top_predictions' in data:
                top3 = data['top_predictions'][:3]
                for i, pred in enumerate(top3[1:], 2):  # Skip first since it's the primary
                    print(f'  #{i}: {pred["disease"]} ({pred["confidence"]*100:.1f}%)')
            print()
        else:
            print(f'{test_name}: API Error {response.status_code}')
    except Exception as e:
        print(f'{test_name}: Connection Error')

# Quick test cases
tests = [
    ('Pneumonia', {'vomiting':40, 'cough':15, 'nasal congestion':16, 'weakness':111, 'sore throat':13}),
    ('Common Cold', {'cough':15, 'nasal congestion':16, 'sore throat':13, 'fever':133, 'headache':41}),
    ('COVID-like', {'fever':133, 'cough':15, 'shortness of breath':2, 'fatigue':111, 'headache':41}),
    ('Heart Attack', {'sharp chest pain':4, 'shortness of breath':2, 'arm pain':57, 'palpitations':9}),
    ('Asthma', {'wheezing':95, 'shortness of breath':2, 'chest tightness':8, 'cough':15}),
    ('Migraine', {'headache':41, 'nausea':42, 'frontal headache':121, 'dizziness':5}),
    ('Food Poisoning', {'vomiting':40, 'diarrhea':43, 'sharp abdominal pain':38, 'nausea':42}),
    ('Depression', {'depressive or psychotic symptoms':3, 'insomnia':6, 'fatigue':111, 'decreased appetite':137}),
    ('Skin Infection', {'skin lesion':71, 'abnormal appearing skin':70, 'skin swelling':20, 'fever':133}),
    ('Diabetes-like', {'frequent urination':49, 'fatigue':111, 'diminished vision':67, 'weight gain':107})
]

print('🩺 DISEASE PREDICTION - 10 TEST CASES')
print('='*50)
for name, symptoms in tests:
    quick_test(symptoms, name)