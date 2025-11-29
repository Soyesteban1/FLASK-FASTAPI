# tickets/tasks.py

from celery import shared_task
from django.utils import timezone
from .models import Ticket, Alert, Customer
from .ml.predict import predict_category
from .ml.churn_model import churn_model
import pandas as pd
from datetime import timedelta

# ---------------------------------------------------------
# 🔥 1. Clasificación de tickets + Alertas automáticas
# ---------------------------------------------------------
@shared_task
def classify_ticket_task(ticket_id):
    """
    Clasifica un ticket usando IA, detecta amenazas y genera alertas proactivas.
    Luego calcula el churn del cliente automáticamente.
    """
    try:
        t = Ticket.objects.get(pk=ticket_id)
    except Ticket.DoesNotExist:
        return "Ticket no existe"

    text = f"{t.title}\n{t.description}".strip().lower()

    # ---------------------------------------------------------
    # 🔹 Clasificación IA
    # ---------------------------------------------------------
    try:
        category = predict_category(text)
        confidence = 1.0
    except Exception:
        category = "unknown"
        confidence = 0.0

    t.category = category
    t.classified = True
    t.metadata = t.metadata or {}
    t.metadata["category_confidence"] = float(confidence)

    # ---------------------------------------------------------
    # 🔹 Detección de amenazas
    # ---------------------------------------------------------
    security_keywords = ["phishing", "ransomware", "sql injection", "ddos", "malware"]

    if any(k in text for k in security_keywords):
        exists = Alert.objects.filter(
            ticket=t, 
            level="critical",
            message="Posible amenaza detectada"
        ).exists()
        if not exists:
            Alert.objects.create(
                ticket=t,
                message="Posible amenaza detectada",
                level="critical",
                handled=False
            )
        t.is_security = True

    # ---------------------------------------------------------
    # 🔹 Alertas proactivas basadas en churn
    # ---------------------------------------------------------
    if hasattr(t.customer, "churn_risk") and t.customer.churn_risk >= 0.7:
        exists = Alert.objects.filter(
            ticket=t, 
            message="Alerta proactiva: riesgo de churn detectado"
        ).exists()
        if not exists:
            Alert.objects.create(
                ticket=t,
                message="Alerta proactiva: riesgo de churn detectado",
                level="critical",
                handled=False
            )

    # ---------------------------------------------------------
    # 🔹 Alertas por tickets repetitivos
    # ---------------------------------------------------------
    one_week_ago = timezone.now() - timedelta(days=7)
    recent_tickets = t.customer.tickets.filter(created_at__gte=one_week_ago).count()

    if recent_tickets >= 3:
        exists = Alert.objects.filter(
            ticket=t,
            message="Cliente con múltiples tickets recientes"
        ).exists()
        if not exists:
            Alert.objects.create(
                ticket=t,
                message="Cliente con múltiples tickets recientes",
                level="warning",
                handled=False
            )

    t.save()

    # ---------------------------------------------------------
    # 🔹 Calcular churn automáticamente
    # ---------------------------------------------------------
    compute_churn_for_customer.delay(t.customer.id)

    return "Clasificación completada"

# ---------------------------------------------------------
# 🔥 2. Cálculo de churn del cliente
# ---------------------------------------------------------
@shared_task
def compute_churn_for_customer(customer_id):
    """
    Calcula el riesgo de churn de un cliente usando su historial de tickets.
    """
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        return "Cliente no existe"

    last_30 = timezone.now() - timedelta(days=30)

    # Features
    recent_count = customer.tickets.filter(created_at__gte=last_30).count()
    high_priority = customer.tickets.filter(priority="high", created_at__gte=last_30).count()
    security_tickets = customer.tickets.filter(is_security=True, created_at__gte=last_30).count()

    # Vector para el modelo como DataFrame
    X = pd.DataFrame(
        [[recent_count, high_priority, security_tickets]],
        columns=['recent_count', 'high_priority', 'security_tickets']
    )

    # ---------------------------------------------------------
    # 🔹 Predicción IA: churn
    # ---------------------------------------------------------
    try:
        risk = churn_model.predict_proba(X)[0][1]  # probabilidad de churn
        risk = float(risk)
    except Exception:
        risk = 0.0

    # Limitar valores entre 0 y 1
    risk = max(0.0, min(risk, 1.0))

    customer.churn_risk = risk
    customer.save()

    return f"Churn actualizado: {risk}"
