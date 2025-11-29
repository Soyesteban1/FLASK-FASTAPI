import os
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.utils import shuffle
import joblib

# Rutas absolutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "tickets_labeled.csv")
MODEL_PATH = os.path.join(BASE_DIR, "ticket_classifier_v1.joblib")

# -----------------------------
# 1. Verificar existencia del CSV
# -----------------------------
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"No existe el archivo de datos: {DATA_PATH}")

df = pd.read_csv(DATA_PATH)

# -----------------------------
# 2. Validar que tenga las columnas necesarias
# -----------------------------
required_cols = ["text", "category"]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"⚠ ERROR: Falta la columna '{col}' en {DATA_PATH}")

# -----------------------------
# 3. Limpiar datos
# -----------------------------
df["text"] = df["text"].fillna("").astype(str)
df = df[df["text"].str.strip() != ""]   # eliminar filas vacías

# Barajar los datos (mejora entrenamiento)
df = shuffle(df, random_state=42)

X = df["text"]
y = df["category"]

# -----------------------------
# 4. Pipeline NLP mejorado
# -----------------------------
pipe = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2),        # usa 1 y 2 palabras (mejor precisión)
        max_features=20000,        # límite razonable
        min_df=1,
        sublinear_tf=True          # suavizado TF-IDF
    )),
    ("clf", LogisticRegression(
        max_iter=2000,
        class_weight="balanced"     # 🔥 mejor rendimiento con pocos ejemplos
    )),
])

# -----------------------------
# 5. Entrenar modelo
# -----------------------------
pipe.fit(X, y)

# -----------------------------
# 6. Guardar modelo
# -----------------------------
joblib.dump(pipe, MODEL_PATH)

print("Modelo entrenado y guardado en:", MODEL_PATH)
