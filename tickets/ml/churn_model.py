# tickets/ml/churn_model.py

import joblib
import os

# Ruta absoluta del archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "churn_model_v1.joblib")

# Cargar el modelo entrenado
try:
    churn_model = joblib.load(MODEL_PATH)
    print(f"[OK] Modelo de churn cargado desde: {MODEL_PATH}")

except Exception as e:
    churn_model = None
    print(f"[ERROR] No se pudo cargar el modelo de churn: {e}")
    print("[INFO] Se utilizará un riesgo de churn = 0.0 como fallback.")


def predict_churn(features):
    """
    Calcula el riesgo de churn usando el modelo.
    features = [recent_count, high_priority, security_tickets]
    """

    if churn_model is None:
        return 0.0  # fallback si no hay modelo cargado

    try:
        # Asegurar que la entrada es correcta
        if not isinstance(features, (list, tuple)) or len(features) != 3:
            print("[WARN] Features inválidos en predict_churn:", features)
            return 0.0

        result = churn_model.predict_proba([features])[0][1]
        return float(result)

    except Exception as e:
        print(f"[ERROR] Falló la predicción de churn: {e}")
        return 0.0
