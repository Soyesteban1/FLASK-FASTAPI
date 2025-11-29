# scripts/process_all.py

import os
import django
import sys

# Añadir la carpeta raíz del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar entorno Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "support_ai.settings")
django.setup()

from tickets.models import Ticket, Customer
from tickets.tasks import classify_ticket_task, compute_churn_for_customer

def process_all_tickets():
    tickets = Ticket.objects.all()
    print(f"Enviando {tickets.count()} tickets a Celery para clasificación...")
    for t in tickets:
        classify_ticket_task.delay(t.id)
    print("Tareas de tickets enviadas.")

def process_all_customers():
    customers = Customer.objects.all()
    print(f"Calculando churn para {customers.count()} clientes...")
    for c in customers:
        compute_churn_for_customer.delay(c.id)
    print("Tareas de churn enviadas.")

if __name__ == "__main__":
    process_all_tickets()
    process_all_customers()
    print("Proceso completo. Verifica en tu Celery worker que las tareas se estén ejecutando.")
