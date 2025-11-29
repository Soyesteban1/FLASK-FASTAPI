import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# --------------------------------------------------
# Rutas absolutas
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "customers_labeled.csv")
MODEL_PATH = os.path.join(BASE_DIR, "churn_model_v1.joblib")

print("------------------------------------------------------")
print(" Entrenamiento del modelo de churn iniciado ")
print("------------------------------------------------------")

# --------------------------------------------------
# Validar existencia del CSV
# --------------------------------------------------
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(
        f"ERROR: No se encontró el archivo de dataset en:\n{DATA_PATH}\n"
        "Asegúrate de que 'customers_labeled.csv' existe en tickets/ml/"
    )

print(f"✔ CSV encontrado en: {DATA_PATH}")

# --------------------------------------------------
# Cargar datos
# --------------------------------------------------
df = pd.read_csv(DATA_PATH)
print(f"✔ Dataset cargado correctamente. Filas: {len(df)}")

required_cols = ["recent_count", "high_priority", "security_tickets", "churn"]
missing = [c for c in required_cols if c not in df.columns]

if missing:
    raise ValueError(
        f"ERROR: Faltan columnas obligatorias en el CSV: {missing}\n"
        f"Columnas encontradas: {list(df.columns)}"
    )

print("✔ Todas las columnas necesarias están presentes.")

# --------------------------------------------------
# Dividir características y etiquetas
# --------------------------------------------------
X = df[["recent_count", "high_priority", "security_tickets"]]
y = df["churn"]

print("✔ Datos preparados para entrenamiento.")
print("Primeras filas de X:")
print(X.head())

# --------------------------------------------------
# Entrenar modelo
# --------------------------------------------------
print("\nEntrenando modelo RandomForest...")

model = RandomForestClassifier(
    n_estimators=150,
    max_depth=7,
    random_state=42
)

model.fit(X, y)

print("✔ Modelo entrenado exitosamente.")

# --------------------------------------------------
# Guardar modelo
# --------------------------------------------------
joblib.dump(model, MODEL_PATH)
print(f"✔ Modelo guardado en: {MODEL_PATH}")

print("------------------------------------------------------")
print(" Entrenamiento completado sin errores ")
print("------------------------------------------------------")
