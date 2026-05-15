# import argparse
# import sys
# import numpy as np
# import pandas as pd
# import tensorflow as tf
# import flwr as fl
# from sklearn.preprocessing import LabelEncoder
# from sklearn.model_selection import train_test_split
# from tensorflow.keras.utils import to_categorical

# # -------------------------
# # Configuration
# # -------------------------
# DEFAULT_EPOCHS = 3
# DEFAULT_BATCH_SIZE = 32
# DEFAULT_SERVER_ADDR = "localhost:8080"

# # -------------------------
# # Model builder
# # -------------------------
# def build_model(input_dim: int, num_classes: int) -> tf.keras.Model:
#     """Build a simple fully-connected NN."""
#     inputs = tf.keras.Input(shape=(input_dim,))
#     x = tf.keras.layers.Dense(128, activation="relu")(inputs)
#     x = tf.keras.layers.Dropout(0.3)(x)
#     x = tf.keras.layers.Dense(64, activation="relu")(x)
#     x = tf.keras.layers.Dropout(0.2)(x)
#     if num_classes == 2:
#         # binary classification
#         outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)
#         loss = "binary_crossentropy"
#         metrics = ["accuracy"]
#     else:
#         # multi-class
#         outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
#         loss = "categorical_crossentropy"
#         metrics = ["accuracy"]

#     model = tf.keras.Model(inputs=inputs, outputs=outputs)
#     model.compile(
#         optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
#         loss=loss,
#         metrics=metrics,
#     )
#     return model

# # -------------------------
# # Data loading / sharding
# # -------------------------
# def load_and_shard_data(
#     csv_path: str, client_id: int, num_clients: int, test_size: float = 0.2, random_state: int = 42
# ):
#     """
#     Load data from CSV, encode labels, and return train+val splits for the client's shard.
#     The dataset is split into `num_clients` shards (roughly equal) after shuffling.
#     Each client receives one shard and performs a local train/test split.
#     """
#     try:
#         df = pd.read_csv("Diseases_and_Symptoms_dataset.csv")
#     except FileNotFoundError:
#         print(f"❌ Error: '{"Diseases_and_Symptoms_dataset.csv"}' not found. Place it in the same folder or give correct path.")
#         sys.exit(1)

#     if "diseases" not in df.columns:
#         print("❌ Error: expected a 'diseases' column in the CSV.")
#         sys.exit(1)

#     # Features and labels
#     X = df.drop("diseases", axis=1).values.astype(np.float32)
#     y = df["diseases"].values.astype(str)

#     # Encode labels
#     le = LabelEncoder()
#     y_enc = le.fit_transform(y)
#     num_classes = len(le.classes_)

#     # Shuffle and shard indices
#     rng = np.random.default_rng(seed=random_state)
#     indices = np.arange(len(X))
#     rng.shuffle(indices)

#     # Compute shard sizes
#     shards = np.array_split(indices, num_clients)
#     if client_id < 0 or client_id >= num_clients:
#         print(f"❌ Error: client_id must be in [0, {num_clients-1}]. Got {client_id}.")
#         sys.exit(1)

#     shard_idx = shards[client_id]
#     X_shard = X[shard_idx]
#     y_shard = y_enc[shard_idx]

#     # Local train/test split for this client
#     if len(X_shard) == 0:
#         print(f"⚠️  Client {client_id} got an empty shard (no data). Exiting.")
#         sys.exit(1)

#     X_train, X_test, y_train, y_test = train_test_split(
#         X_shard, y_shard, test_size=test_size, random_state=random_state, stratify=y_shard if len(np.unique(y_shard))>1 else None
#     )

#     # Convert labels to categorical if multi-class
#     if num_classes == 2:
#         y_train_processed = y_train  # binary (0/1)
#         y_test_processed = y_test
#     else:
#         y_train_processed = to_categorical(y_train, num_classes=num_classes)
#         y_test_processed = to_categorical(y_test, num_classes=num_classes)

#     return (X_train, y_train_processed), (X_test, y_test_processed), num_classes, le

# # -------------------------
# # Flower NumPyClient
# # -------------------------
# class KerasFlowerClient(fl.client.NumPyClient):
#     def __init__(self, model: tf.keras.Model, train_data, test_data, epochs=DEFAULT_EPOCHS, batch_size=DEFAULT_BATCH_SIZE):
#         self.model = model
#         self.X_train, self.y_train = train_data
#         self.X_test, self.y_test = test_data
#         self.epochs = epochs
#         self.batch_size = batch_size

#     def get_parameters(self, config):
#         # Return model weights as a list of NumPy arrays
#         return self.model.get_weights()

#     def fit(self, parameters, config):
#         # Set model weights, train locally, return updated weights
#         if parameters is not None:
#             self.model.set_weights(parameters)
#         # Train
#         self.model.fit(self.X_train, self.y_train, epochs=self.epochs, batch_size=self.batch_size, verbose=1)
#         # Return updated weights and number of local examples
#         return self.model.get_weights(), len(self.X_train), {}

#     def evaluate(self, parameters, config):
#         # Set model weights, evaluate on local test set, return loss and metrics
#         if parameters is not None:
#             self.model.set_weights(parameters)
#         loss, *rest = self.model.evaluate(self.X_test, self.y_test, batch_size=self.batch_size, verbose=0)
#         # Keras returns loss + metric values; we extract accuracy if present
#         metrics = {}
#         if len(rest) >= 1:
#             metrics["accuracy"] = float(rest[0])
#         else:
#             # maybe metric name different; try predict-then-accuracy
#             preds = self.model.predict(self.X_test, batch_size=self.batch_size)
#             if preds.shape[-1] == 1:
#                 acc = (preds.ravel() > 0.5) == self.y_test
#                 metrics["accuracy"] = float(np.mean(acc))
#             else:
#                 metrics["accuracy"] = float(np.mean(np.argmax(preds, axis=1) == np.argmax(self.y_test, axis=1)))
#         return float(loss), len(self.X_test), metrics

# # -------------------------
# # CLI and main
# # -------------------------
# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--csv", type=str, default="Diseases_and_Symptoms_dataset.csv", help="Path to CSV file")
#     parser.add_argument("--client-id", type=int, default=0, help="Client id (0-indexed)")
#     parser.add_argument("--num-clients", type=int, default=1, help="Total number of clients to shard the dataset into")
#     parser.add_argument("--epochs", type=int, default=DEFAULT_EPOCHS, help="Local epochs per fit()")
#     parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE, help="Local batch size")
#     parser.add_argument("--server-address", type=str, default=DEFAULT_SERVER_ADDR, help="Flower server address")
#     return parser.parse_args()

# def main():
#     args = parse_args()
#     # Load/shard data
#     (X_train, y_train), (X_test, y_test), num_classes, label_encoder = load_and_shard_data(
#         args.csv, args.client_id, args.num_clients
#     )
#     input_dim = X_train.shape[1]
#     print(f"[Client {args.client_id}] Data shapes -- X_train: {X_train.shape}, y_train: {y_train.shape}; classes: {num_classes}")

#     # Build model
#     model = build_model(input_dim, num_classes)
#     model.summary()

#     # Optional: warm-start (fit once to initialize weights) - not strictly necessary
#     # model.fit(X_train[:min(32,len(X_train))], y_train[:min(32,len(y_train))], epochs=1, verbose=0)

#     # Create Flower client
#     client = KerasFlowerClient(model=model, train_data=(X_train, y_train), test_data=(X_test, y_test),
#                                epochs=args.epochs, batch_size=args.batch_size)

#     # Start client and connect to server
#     print(f"[Client {args.client_id}] Connecting to Flower server at {args.server_address} ...")
#     fl.client.start_numpy_client(server_address=args.server_address, client=client)

# if __name__ == "__main__":
#     main()



import argparse
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import flwr as fl
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

# -------------------------
# Configuration
# -------------------------
DEFAULT_EPOCHS = 3
DEFAULT_BATCH_SIZE = 32
DEFAULT_SERVER_ADDR = "localhost:8080"
MODEL_WEIGHTS_PATH = "global_model.weights.h5"

# -------------------------
# Model builder
# -------------------------
def build_model(input_dim: int, num_classes: int) -> tf.keras.Model:
    inputs = tf.keras.Input(shape=(input_dim,))
    x = tf.keras.layers.Dense(128, activation="relu")(inputs)
    x = tf.keras.layers.Dropout(0.3)(x)
    x = tf.keras.layers.Dense(64, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.2)(x)

    if num_classes == 2:
        outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)
        loss = "binary_crossentropy"
        metrics = ["accuracy"]
    else:
        outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
        loss = "categorical_crossentropy"
        metrics = ["accuracy"]

    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss=loss,
        metrics=metrics,
    )
    return model

# -------------------------
# Data loading / sharding
# -------------------------
def load_and_shard_data(csv_path, client_id, num_clients, test_size=0.2, random_state=42):
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"❌ CSV file not found: {csv_path}")
        sys.exit(1)

    if "diseases" not in df.columns:
        print("❌ Expected 'diseases' column in CSV")
        sys.exit(1)

    feature_names = list(df.drop("diseases", axis=1).columns)

    X = df.drop("diseases", axis=1).values.astype(np.float32)
    y = df["diseases"].astype(str).values

    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    num_classes = len(le.classes_)

    rng = np.random.default_rng(seed=random_state)
    indices = np.arange(len(X))
    rng.shuffle(indices)
    shards = np.array_split(indices, num_clients)

    if client_id < 0 or client_id >= num_clients:
        print("❌ Invalid client_id")
        sys.exit(1)

    shard_idx = shards[client_id]
    X_shard = X[shard_idx]
    y_shard = y_enc[shard_idx]

    X_train, X_test, y_train, y_test = train_test_split(
        X_shard,
        y_shard,
        test_size=test_size,
        random_state=random_state,
        stratify=y_shard if len(np.unique(y_shard)) > 1 else None,
    )

    if num_classes == 2:
        y_train = y_train
        y_test = y_test
    else:
        y_train = to_categorical(y_train, num_classes)
        y_test = to_categorical(y_test, num_classes)

    return (X_train, y_train), (X_test, y_test), num_classes, le, feature_names

# -------------------------
# Flower Client
# -------------------------
class KerasFlowerClient(fl.client.NumPyClient):
    def __init__(self, model, train_data, test_data, epochs, batch_size):
        self.model = model
        self.X_train, self.y_train = train_data
        self.X_test, self.y_test = test_data
        self.epochs = epochs
        self.batch_size = batch_size

    def get_parameters(self, config):
        return self.model.get_weights()

    def fit(self, parameters, config):
        self.model.set_weights(parameters)
        self.model.fit(
            self.X_train,
            self.y_train,
            epochs=self.epochs,
            batch_size=self.batch_size,
            verbose=1,
        )
        # Save latest global-ish model (for inference testing)
        self.model.save_weights(MODEL_WEIGHTS_PATH)
        return self.model.get_weights(), len(self.X_train), {}

    def evaluate(self, parameters, config):
        self.model.set_weights(parameters)
        loss, acc = self.model.evaluate(self.X_test, self.y_test, verbose=0)
        return float(loss), len(self.X_test), {"accuracy": float(acc)}

# -------------------------
# Terminal inference helpers
# -------------------------
def take_symptom_input(feature_names):
    print("\nEnter symptoms (1 = Yes, 0 = No)\n")
    values = []
    for name in feature_names:
        while True:
            v = input(f"{name} (0/1): ").strip()
            if v in ("0", "1"):
                values.append(int(v))
                break
            print("❌ Enter 0 or 1 only")
    return np.array(values, dtype=np.float32).reshape(1, -1)

def run_terminal_inference(model, label_encoder, feature_names):
    x = take_symptom_input(feature_names)
    preds = model.predict(x)

    if preds.shape[1] == 1:
        prob = float(preds[0][0])
        idx = int(prob > 0.5)
        confidence = prob
    else:
        idx = int(np.argmax(preds[0]))
        confidence = float(preds[0][idx])

    disease = label_encoder.inverse_transform([idx])[0]

    print("\n🧠 Prediction Result")
    print("-------------------")
    print(f"Disease    : {disease}")
    print(f"Confidence : {confidence:.4f}")

# -------------------------
# CLI
# -------------------------
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["train", "infer"], default="train")
    parser.add_argument("--csv", type=str, default="Diseases_and_Symptoms_dataset.csv")
    parser.add_argument("--client-id", type=int, default=0)
    parser.add_argument("--num-clients", type=int, default=1)
    parser.add_argument("--epochs", type=int, default=DEFAULT_EPOCHS)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--server-address", type=str, default=DEFAULT_SERVER_ADDR)
    return parser.parse_args()

# -------------------------
# Main
# -------------------------
def main():
    args = parse_args()

    (X_train, y_train), (X_test, y_test), num_classes, label_encoder, feature_names = load_and_shard_data(
        args.csv, args.client_id, args.num_clients
    )

    model = build_model(X_train.shape[1], num_classes)
    model.summary()

    if args.mode == "train":
        client = KerasFlowerClient(
            model,
            (X_train, y_train),
            (X_test, y_test),
            args.epochs,
            args.batch_size,
        )
        print(f"[Client {args.client_id}] Connecting to Flower server at {args.server_address}")
        fl.client.start_numpy_client(server_address=args.server_address, client=client)

    else:
        model.load_weights(MODEL_WEIGHTS_PATH)
        print("✅ Loaded trained model")
        run_terminal_inference(model, label_encoder, feature_names)

if __name__ == "__main__":
    main()
