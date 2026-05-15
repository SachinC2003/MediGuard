import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from model_service import predict_disease
import json
import os

app = Flask(__name__)
CORS(app)

# Load correct disease names from dataset
disease_names_file = "disease_names.json"
if os.path.exists(disease_names_file):
    with open(disease_names_file, 'r') as f:
        DISEASE_NAMES = json.load(f)
    print(f"✅ Loaded {len(DISEASE_NAMES)} disease names from {disease_names_file}")
else:
    print("⚠️  WARNING: disease_names.json not found. Using default list.")
    # Fallback to generated list from dataset
    DISEASE_NAMES = [
        "actinic keratosis", "acute bronchiolitis", "acute bronchitis", "acute bronchospasm", 
        "acute kidney injury", "acute pancreatitis", "acute sinusitis", "allergy", "angina", 
        "anxiety", "appendicitis", "arthritis of the hip", "asthma", "benign prostatic hyperplasia (bph)", 
        "brachial neuritis", "bursitis", "carpal tunnel syndrome", "cholecystitis", "chronic back pain", 
        "chronic constipation", "chronic obstructive pulmonary disease (copd)", "common cold", 
        "complex regional pain syndrome", "concussion", "conjunctivitis", "conjunctivitis due to allergy", 
        "contact dermatitis", "cornea infection", "croup", "cystitis", "degenerative disc disease", 
        "dental caries", "depression", "developmental disability", "diaper rash", "diverticulitis", 
        "drug reaction", "ear drum damage", "eczema", "esophagitis", "eustachian tube dysfunction (ear disorder)", 
        "fungal infection of the hair", "gallstone", "gastrointestinal hemorrhage", "gout", "gum disease", 
        "heart attack", "heart failure", "hemorrhoids", "herniated disk", "hiatal hernia", 
        "hyperemesis gravidarum", "hypertensive heart disease", "hypoglycemia", "idiopathic excessive menstruation", 
        "idiopathic irregular menstrual cycle", "idiopathic painful menstruation", "infectious gastroenteritis", 
        "injury to the arm", "injury to the leg", "injury to the trunk", "liver disease", "macular degeneration", 
        "marijuana abuse", "multiple sclerosis", "noninfectious gastroenteritis", "nose disorder", 
        "obstructive sleep apnea (osa)", "otitis externa (swimmer's ear)", "otitis media", "pain after an operation", 
        "panic disorder", "pelvic inflammatory disease", "peripheral nerve disorder", "personality disorder", 
        "pneumonia", "problem during pregnancy", "psoriasis", "pyogenic skin infection", "rectal disorder", 
        "schizophrenia", "seasonal allergies (hay fever)", "sebaceous cyst", "sepsis", "sickle cell crisis", 
        "sinus bradycardia", "skin pigmentation disorder", "skin polyp", "spinal stenosis", "spondylosis", 
        "spontaneous abortion", "sprain or strain", "strep throat", "stye", "temporary or benign blood in urine", 
        "threatened pregnancy", "urinary tract infection", "vaginal cyst", "vaginitis", "vulvodynia"
    ]

@app.route('/')
def home():
    return jsonify({
        "message": "Health Prediction API is running.",
        "num_diseases": len(DISEASE_NAMES),
        "num_features": 230
    })
     

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 1. Extract data from React request
        data = request.json.get('features')
        top_k = request.json.get('return_top_k', 1)  # Default to 1, but allow more

        # 2. Validation
        if not data or len(data) != 230:
            return jsonify({
                "error": f"Expected 230 features, got {len(data) if data else 0}"
            }), 400

        # 3. Get Prediction from Model
        # predict_disease returns probabilities array of shape (100,)
        raw_prediction = predict_disease(data)

        # 4. Process the results
        class_index = int(np.argmax(raw_prediction))
        confidence = float(np.max(raw_prediction))

        # 5. Map index to Disease Name
        if class_index < len(DISEASE_NAMES):
            predicted_disease = DISEASE_NAMES[class_index]
        else:
            predicted_disease = f"Unknown Condition (Class {class_index})"

        # 6. Return response to React
        response = {
            "disease": predicted_disease,
            "confidence": confidence,
            "class_index": class_index
        }

        # Add top predictions if requested
        if top_k > 1:
            response["top_predictions"] = get_top_predictions(raw_prediction, top_k)

        return jsonify(response)

    except Exception as e:
        print(f"🔥 Backend Crash: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

def get_top_predictions(probabilities, top_n=5):
    """Get top N predictions with disease names and probabilities"""
    top_indices = np.argsort(probabilities)[-top_n:][::-1]
    results = []
    for idx in top_indices:
        disease_name = DISEASE_NAMES[idx] if idx < len(DISEASE_NAMES) else f"Unknown (Class {idx})"
        results.append({
            "disease": disease_name,
            "confidence": float(probabilities[idx]),
            "index": int(idx)
        })
    return results

if __name__ == "__main__":
    app.run(port=5000, debug=True)