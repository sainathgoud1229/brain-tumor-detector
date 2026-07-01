from pathlib import Path
import pickle
import sys

import numpy as np
import tensorflow as tf

try:
    import keras
    load_model = keras.models.load_model
except ImportError:
    load_model = tf.keras.models.load_model

CURRENT_DIR = Path(__file__).resolve().parent

if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from preprocessing import prepare_image

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = PROJECT_ROOT / "models" / "best_model.keras"
CLASS_PATH = PROJECT_ROOT / "models" / "class_names.pkl"

model = load_model(MODEL_PATH, compile=False)

with open(CLASS_PATH, "rb") as file:
    CLASS_NAMES = pickle.load(file)


def predict(image_path):
    image = prepare_image(image_path)

    prediction = model.predict(image, verbose=0)

    predicted_index = np.argmax(prediction)

    confidence = float(np.max(prediction))

    return {
        "predicted_class": CLASS_NAMES[predicted_index],
        "confidence": round(confidence * 100, 2),
        "probabilities": {
            CLASS_NAMES[i]: round(float(prediction[0][i]) * 100, 2)
            for i in range(len(CLASS_NAMES))
        }
    }


if __name__ == "__main__":
    image_path = input("Enter MRI Image Path: ")

    result = predict(image_path)

    print("\nPrediction Result\n")

    print(result)