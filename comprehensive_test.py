import requests
import json

# Load disease names for reference
with open('flask-backend/disease_names.json', 'r') as f:
    DISEASES = json.load(f)

def test_prediction(symptoms_dict, test_name):
    """Test a prediction with given symptoms"""
    features = [0] * 230

    # Set the symptom indices to 1
    for symptom, index in symptoms_dict.items():
        features[index] = 1

    print(f"\n{'='*60}")
    print(f"🧪 TEST CASE: {test_name}")
    print(f"{'='*60}")
    print(f"Symptoms: {', '.join(symptoms_dict.keys())}")
    print(f"Indices: {list(symptoms_dict.values())}")

    try:
        response = requests.post('http://localhost:5000/predict',
                               json={'features': features},
                               headers={'Content-Type': 'application/json'},
                               timeout=10)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Disease: {data['disease']}")
            print(f"✅ Confidence: {data['confidence']*100:.2f}%")

            # Get top 3 predictions for more insight
            response_full = requests.post('http://localhost:5000/predict',
                                        json={'features': features, 'return_top_k': 3},
                                        headers={'Content-Type': 'application/json'},
                                        timeout=10)

            if response_full.status_code == 200:
                full_data = response_full.json()
                if 'top_predictions' in full_data:
                    print("📊 Top 3 predictions:")
                    for i, pred in enumerate(full_data['top_predictions'], 1):
                        print(f"   {i}. {pred['disease']}: {pred['confidence']*100:.2f}%")

        else:
            print(f"❌ API Error: {response.status_code}")

    except Exception as e:
        print(f"❌ Connection Error: {e}")

# Test Cases
test_cases = [
    {
        "name": "Pneumonia Symptoms",
        "symptoms": {
            "vomiting": 40,
            "cough": 15,
            "nasal congestion": 16,
            "weakness": 111,
            "sore throat": 13
        }
    },
    {
        "name": "Common Cold",
        "symptoms": {
            "cough": 15,
            "nasal congestion": 16,
            "sore throat": 13,
            "fever": 133,
            "headache": 41
        }
    },
    {
        "name": "Respiratory Infection (COVID-like)",
        "symptoms": {
            "fever": 133,
            "cough": 15,
            "shortness of breath": 2,
            "fatigue": 111,  # weakness
            "headache": 41
        }
    },
    {
        "name": "Heart Attack Symptoms",
        "symptoms": {
            "sharp chest pain": 4,
            "shortness of breath": 2,
            "arm pain": 57,
            "palpitations": 9
        }
    },
    {
        "name": "Diabetes Symptoms",
        "symptoms": {
            "frequent urination": 49,
            "increased thirst": 111,  # weakness/fatigue
            "blurred vision": 67,  # diminished vision
            "fatigue": 111
        }
    },
    {
        "name": "Asthma Attack",
        "symptoms": {
            "wheezing": 95,
            "shortness of breath": 2,
            "chest tightness": 8,
            "cough": 15
        }
    },
    {
        "name": "Migraine Headache",
        "symptoms": {
            "headache": 41,
            "nausea": 42,
            "frontal headache": 121,
            "dizziness": 5
        }
    },
    {
        "name": "Food Poisoning",
        "symptoms": {
            "vomiting": 40,
            "diarrhea": 43,
            "sharp abdominal pain": 38,
            "nausea": 42
        }
    },
    {
        "name": "Depression Symptoms",
        "symptoms": {
            "depressive or psychotic symptoms": 3,
            "insomnia": 6,
            "fatigue": 111,
            "decreased appetite": 137
        }
    },
    {
        "name": "Skin Infection",
        "symptoms": {
            "skin lesion": 71,
            "abnormal appearing skin": 70,
            "skin swelling": 20,
            "fever": 133
        }
    }
]

if __name__ == "__main__":
    print("🩺 DISEASE PREDICTION SYSTEM - COMPREHENSIVE TESTING")
    print("Testing 10 different symptom combinations...")
    print("Make sure Flask backend is running on http://localhost:5000/")

    for test_case in test_cases:
        test_prediction(test_case["symptoms"], test_case["name"])

    print(f"\n{'='*60}")
    print("🎯 TESTING COMPLETE!")
    print("All predictions should be medically reasonable for the given symptoms.")
    print(f"{'='*60}")




# 10 Test Cases to Try in the Browser





#--------------------------------------------------------------------
#-------------------------------------------------------------------
#shortness of breath, chest tightness, palpitations, irregular heartbeat, breathing fast
#Correct disease: panic disorder

#suprapubic pain, vaginal itching, painful urination, pain during intercourse, vaginal pain
#Correct disease: vaginitis

#sharp abdominal pain, vomiting, nausea, lower abdominal pain, spotting or bleeding during pregnancy
#Correct disease: problem during pregnancy

#vomiting, diarrhea, side pain, hemoptysis
#Correct disease: acute pancreatitis

#sharp chest pain, wheezing, fever, coughing up sputum, allergic reaction
#Correct disease: asthma

#blood in stool, sharp abdominal pain, vomiting, nausea, diarrhea
#Correct disease: non-infectious gastroenteritis

#sore throat, ear pain, frontal headache, fever, sinus congestion
#Correct disease: acute sinusitis

#diminished vision, pain in eye, spots or clouds in vision, eye redness, lacrimation
#Correct disease: cornea infection

#leg pain, arm stiffness or tightness, knee swelling, elbow swelling
#Correct disease: bursitis

#leg pain, hip pain, neck pain, low back pain, loss of sensation
#Correct disease: spondylosis

#hand or finger pain, arm pain, bones are painful, loss of sensation, elbow swelling
#Correct disease: injury to the arm

#leg pain, hand or finger pain, foot or toe pain, ache all over
#Correct disease: complex regional pain syndrome

#headache, back pain, neck pain, shoulder pain, rib pain
#Correct disease: injury to the trunk

#nausea, back pain, pelvic pain, burning abdominal pain, side pain
#Correct disease: vulvodynia

#dizziness, difficulty speaking, headache, nausea, rib pain
#Correct disease: concussion

#dizziness, abnormal involuntary movements, feeling ill, nausea, problems with movement
#Correct disease: hypoglycemia