# tickets/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket, Customer
from .tasks import classify_ticket_task, compute_churn_for_customer

@receiver(post_save, sender=Ticket)
def handle_new_ticket(sender, instance, created, **kwargs):
    """
    Signal que se ejecuta al crear un ticket:
    - Envía el ticket a Celery para clasificación y detección de amenazas
    - Recalcula riesgo de churn del cliente automáticamente
    """
    if created:
        # Enviar ticket a Celery para clasificación IA
        classify_ticket_task.delay(instance.id)

        # Recalcular churn del cliente automáticamente
        if instance.customer_id:
            compute_churn_for_customer.delay(instance.customer_id)
