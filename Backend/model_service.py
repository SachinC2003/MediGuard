import tensorflow as tf
import numpy as np
import pickle
import os

def create_model(input_dim=230, num_classes=100):
    """
    Create model with correct architecture matching federated learning setup
    """
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(shape=(input_dim,)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    return model

# Initialize model
MODEL = create_model(input_dim=230, num_classes=100)

# Load weights - try multiple possible file names
weight_files = ["global_model.weights.h5", "trained_model.h5", "trained_model2.h5"]
loaded = False
for weight_file in weight_files:
    if os.path.exists(weight_file):
        try:
            MODEL.load_weights(weight_file)
            print(f"✅ Loaded weights from {weight_file}")
            loaded = True
            break
        except Exception as e:
            print(f"⚠️ Failed to load {weight_file}: {e}")

if not loaded:
    print("⚠️  WARNING: No valid model weights found. Using random initialization.")

def predict_disease(features):
    """
    Predict disease from 230-feature binary vector
    Returns: numpy array of shape (1, 100) with probabilities for each disease
    """
    # Reshape features for the model (1 sample, 230 features)
    input_data = np.array(features, dtype=np.float32).reshape(1, 230)
    
    # Get probabilities for all classes
    prediction = MODEL.predict(input_data, verbose=0)
    return prediction[0]  # Return 1D array of probabilities