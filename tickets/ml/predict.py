# tickets/ml/predict.py

import os
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "ticket_classifier_v1.joblib")

# Cargar modelo solo una vez
try:
    pipe = joblib.load(MODEL_PATH)
except Exception:
    pipe = None
    print("⚠ No se pudo cargar el modelo ticket_classifier_v1.joblib")

def predict_category(text):
    """
    Clasifica tickets en categorías usando NLP.
    Debe devolver: technical / billing / account / security / other
    """
    if not text or pipe is None:
        return "unknown"

    try:
        pred = pipe.predict([text])[0]
        return str(pred)
    except Exception as e:
        print("Error al predecir categoría:", e)
        return "unknown"
