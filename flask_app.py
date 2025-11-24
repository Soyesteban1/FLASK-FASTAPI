# flask_app.py
from flask import Flask, render_template, request, redirect, session, url_for
import requests

app = Flask(__name__)
app.secret_key = "FLASK_SECRET_KEY_CHANGE_ME"

FASTAPI_URL = "http://127.0.0.1:8000"


def login_required(f):#esta funcion hacemos el login
    def wrapper(*args, **kwargs):
        if "token" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


def safe_post(url, json=None, headers=None):
    """Envía un POST seguro y devuelve (status_code, data o None, error_message)"""
    try:
        r = requests.post(url, json=json, headers=headers)
    except requests.exceptions.RequestException as e:
        return None, None, f"No se pudo conectar al servidor: {e}"
    try:
        data = r.json()
    except ValueError:
        data = None
    if r.status_code != 200:
        msg = data.get("detail") if data else f"Error {r.status_code}"
        return r.status_code, data, msg
    return r.status_code, data, None


def safe_get(url, headers=None):
    """Envía un GET seguro y devuelve data o lista vacía si falla"""
    try:
        r = requests.get(url, headers=headers)
    except requests.exceptions.RequestException:
        return []
    try:
        data = r.json()
    except ValueError:
        return []
    if r.status_code != 200:
        return []
    return data


def safe_delete(url, headers=None):
    """Envía un DELETE seguro"""
    try:
        r = requests.delete(url, headers=headers)
    except requests.exceptions.RequestException:
        return False
    return r.status_code == 200


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        status, data, msg = safe_post(f"{FASTAPI_URL}/auth/login", json={"email": email, "password": password})
        if msg:
            return render_template("login.html", error=msg)

        session["token"] = data.get("access_token")
        session["rol"] = data.get("rol")
        return redirect(url_for("dashboard"))

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def dashboard():
    token = session.get("token")
    headers = {"Authorization": f"Bearer {token}"}

    estudiantes = safe_get(f"{FASTAPI_URL}/estudiantes/listar", headers=headers)
    profesores = safe_get(f"{FASTAPI_URL}/profesores/listar", headers=headers)

    return render_template("dashboard.html", estudiantes=estudiantes, profesores=profesores)


@app.route("/agregar", methods=["POST"])
@login_required
def agregar():
    tipo = request.form.get("tipo")  # "estudiante" o "profesor"
    token = session.get("token")
    headers = {"Authorization": f"Bearer {token}"}

    if tipo == "estudiante":
        data = {
            "nombre": request.form.get("nombre"),
            "apellido": request.form.get("apellido"),
            "edad": int(request.form.get("edad") or 0),
            "curso": request.form.get("materia")
        }
        safe_post(f"{FASTAPI_URL}/estudiantes/agregar", json=data, headers=headers)
    else:
        data = {
            "nombre": request.form.get("nombre"),
            "apellido": request.form.get("apellido"),
            "curso": request.form.get("materia")
        }
        safe_post(f"{FASTAPI_URL}/profesores/agregar", json=data, headers=headers)

    return redirect(url_for("dashboard"))


@app.route("/buscar", methods=["GET"])
@login_required
def buscar():
    q = request.args.get("q", "")
    token = session.get("token")
    headers = {"Authorization": f"Bearer {token}"}

    estudiantes = safe_get(f"{FASTAPI_URL}/estudiantes/listar", headers=headers)
    profesores = safe_get(f"{FASTAPI_URL}/profesores/listar", headers=headers)

    estudiantes_f = [e for e in estudiantes if q.lower() in (e.get("nombre", "") + " " + e.get("apellido", "")).lower()]
    profesores_f = [p for p in profesores if q.lower() in (p.get("nombre", "") + " " + p.get("apellido", "")).lower()]

    return render_template("dashboard.html", estudiantes=estudiantes_f, profesores=profesores_f, q=q)


@app.route("/eliminar/<tipo>/<int:id>", methods=["POST"])
@login_required
def eliminar(tipo, id):
    token = session.get("token")
    headers = {"Authorization": f"Bearer {token}"}
    if tipo == "estudiante":
        safe_delete(f"{FASTAPI_URL}/estudiantes/eliminar/{id}", headers=headers)
    else:
        safe_delete(f"{FASTAPI_URL}/profesores/eliminar/{id}", headers=headers)
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
