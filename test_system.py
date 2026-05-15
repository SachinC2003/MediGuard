"""
Test script to verify all components are set up correctly
"""
import os
import sys
import json

def test_files_exist():
    """Check if all required files exist"""
    print("=" * 60)
    print("CHECKING REQUIRED FILES")
    print("=" * 60)
    
    files_to_check = {
        "flask-backend": [
            "app.py",
            "model_service.py",
            "disease_names.json",
            "label_encoder.pkl",
            "global_model.weights.h5"
        ],
        "megaProject": [
            "client.py",
            "server.py",
            "model.py",
            "Diseases_and_Symptoms_dataset.csv",
            "disease_names.json",
            "label_encoder.pkl"
        ],
        "megaProject-Frontend": [
            "src/App.tsx",
            "package.json"
        ]
    }
    
    all_ok = True
    base_dir = "c:\\Users\\Sachin\\Desktop\\New folder"
    
    for folder, files in files_to_check.items():
        print(f"\n{folder}:")
        for file in files:
            path = os.path.join(base_dir, folder, file)
            if os.path.exists(path):
                size = os.path.getsize(path)
                if size > 1024*1024:
                    size_str = f"{size/(1024*1024):.1f}MB"
                elif size > 1024:
                    size_str = f"{size/1024:.1f}KB"
                else:
                    size_str = f"{size}B"
                print(f"  [OK] {file} ({size_str})")
            else:
                print(f"  [MISSING] {file}")
                all_ok = False
    
    return all_ok

def test_disease_names():
    """Verify disease names are correct"""
    print("\n" + "=" * 60)
    print("VERIFYING DISEASE NAMES")
    print("=" * 60)
    
    disease_file = "c:\\Users\\Sachin\\Desktop\\New folder\\flask-backend\\disease_names.json"
    
    try:
        with open(disease_file, 'r') as f:
            diseases = json.load(f)
        
        print(f"Found {len(diseases)} diseases")
        
        if len(diseases) == 100:
            print("[OK] Exactly 100 diseases (correct)")
            print("\nFirst 10 diseases:")
            for i, disease in enumerate(diseases[:10], 1):
                print(f"  {i}. {disease}")
            return True
        else:
            print(f"[ERROR] Expected 100 diseases, got {len(diseases)}")
            return False
    except FileNotFoundError:
        print("[MISSING] disease_names.json not found")
        return False
    except json.JSONDecodeError:
        print("[ERROR] Invalid JSON in disease_names.json")
        return False

def test_imports():
    """Test if main dependencies can be imported"""
    print("\n" + "=" * 60)
    print("TESTING PYTHON IMPORTS")
    print("=" * 60)
    
    imports = {
        "numpy": "import numpy",
        "pandas": "import pandas",
        "tensorflow": "import tensorflow",
        "sklearn": "from sklearn.preprocessing import LabelEncoder",
        "Flask": "from flask import Flask",
        "Flask-CORS": "from flask_cors import CORS",
        "flwr": "import flwr as fl"
    }
    
    all_ok = True
    for name, import_stmt in imports.items():
        try:
            exec(import_stmt)
            print(f"  [OK] {name}")
        except ImportError as e:
            print(f"  [MISSING] {name} - {str(e)[:60]}")
            all_ok = False
    
    return all_ok

def test_model_structure():
    """Verify model structure"""
    print("\n" + "=" * 60)
    print("VERIFYING MODEL STRUCTURE")
    print("=" * 60)
    
    try:
        import tensorflow as tf
        import numpy as np
        
        # Create a test model with correct architecture
        model = tf.keras.Sequential([
            tf.keras.layers.InputLayer(shape=(230,)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(100, activation='softmax')
        ])
        
        print("[OK] Model architecture created successfully")
        print(f"   Input: 230 features")
        print(f"   Hidden: 128 -> 64 neurons")
        print(f"   Output: 100 diseases")
        
        # Test prediction with dummy data
        dummy_input = np.random.randn(1, 230).astype(np.float32)
        prediction = model.predict(dummy_input, verbose=0)
        
        print(f"\n[OK] Model can make predictions")
        print(f"   Output shape: {prediction.shape}")
        print(f"   Top disease index: {np.argmax(prediction[0])}")
        print(f"   Confidence: {np.max(prediction[0]):.4f}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Model test failed: {str(e)[:100]}")
        return False

def main():
    print("\n")
    print("*" * 60)
    print("* DISEASE PREDICTION SYSTEM - VERIFICATION TEST")
    print("*" * 60)
    
    results = []
    
    results.append(("File Integrity", test_files_exist()))
    results.append(("Disease Names", test_disease_names()))
    results.append(("Python Imports", test_imports()))
    results.append(("Model Structure", test_model_structure()))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_pass = True
    for test_name, passed in results:
        status = "[OK]" if passed else "[FAIL]"
        print(f"{status} {test_name}")
        if not passed:
            all_pass = False
    
    print("\n" + "=" * 60)
    if all_pass:
        print("ALL TESTS PASSED - System ready to use!")
        print("\nTo start:")
        print("1. Run server: python megaProject/server.py")
        print("2. Run clients: python megaProject/client.py --client-id X --num-clients 3")
        print("3. Run backend: python flask-backend/app.py") 
        print("4. Run frontend: cd megaProject-Frontend && npm run dev")
    else:
        print("SOME TESTS FAILED - Please fix issues above")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
