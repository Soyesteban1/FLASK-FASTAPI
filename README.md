# Support AI

Support AI es un proyecto desarrollado en Django 5.2 que tiene como objetivo **automatizar y mejorar la gestión de soporte al cliente** mediante inteligencia artificial y herramientas web.  
El proyecto permite crear, clasificar y gestionar tickets de soporte, así como integrar alertas y notificaciones, todo desde una interfaz web limpia y organizada.

---

## **Características**

- Gestión de tickets de soporte.
- Clasificación automática de tickets por categoría.
- Integración de alertas y notificaciones.
- Interfaz web intuitiva con templates HTML.
- Preparado para extensiones con archivos estáticos (CSS/JS) en caso de ser necesario.
- Estructura modular siguiendo buenas prácticas de Django.

---

## **Estructura del proyecto**

support_ai/
├─ manage.py
├─ support_ai/ # Configuración principal de Django
│ ├─ settings.py
│ ├─ urls.py
│ └─ wsgi.py
├─ app1/ # Tu aplicación de soporte
│ ├─ models.py
│ ├─ views.py
│ ├─ migrations/
│ └─ ...
├─ templates/ # HTML del proyecto
│ └─ *.html
├─ static/ # Opcional: CSS, JS, imágenes
│ └─ ...
├─ requirements.txt # Dependencias del proyecto
└─ README.md

1. Clonar el repositorio:

```bash
git clone https://github.com/Soyesteban1/support_ai.git
cd support_ai
Crear un entorno virtual:

bash
Copiar código
python -m venv env
source env/bin/activate  # Linux / macOS
env\Scripts\activate     # Windows
Instalar dependencias:

bash
Copiar código
pip install -r requirements.txt
Aplicar migraciones de Django:

bash
Copiar código
python manage.py migrate
Ejecutar el servidor de desarrollo:

bash
Copiar código
python manage.py runserver
Abrir el proyecto en tu navegador:

cpp
Copiar código
http://127.0.0.1:8000/
