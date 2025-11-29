from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High')
]

# -----------------------------------------------------------
# CUSTOMER
# -----------------------------------------------------------
class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    company = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)   # <-- FECHA AWARE
    churn_risk = models.FloatField(default=0.0)               # riesgo 0–1

    def __str__(self):
        return f"{self.name} ({self.company})"


# -----------------------------------------------------------
# TICKET
# -----------------------------------------------------------
class Ticket(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    title = models.CharField(max_length=300)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True, null=True)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='low'
    )
    created_at = models.DateTimeField(default=timezone.now)   # <-- FIX
    classified = models.BooleanField(default=False)
    is_security = models.BooleanField(default=False)
    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Ticket {self.id} - {self.title[:30]}"


# -----------------------------------------------------------
# ALERT
# -----------------------------------------------------------
class Alert(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='alerts'
    )
    message = models.CharField(max_length=400)
    level = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)  # <-- FIX
    handled = models.BooleanField(default=False)

    def __str__(self):
        return f"Alert {self.id} - {self.level}"


# -----------------------------------------------------------
# MODEL RECORD (opcional para modelos ML)
# -----------------------------------------------------------
class ModelRecord(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    path = models.CharField(max_length=400)
    trained_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} (v{self.version})"


# -----------------------------------------------------------
# SIGNALS → Enviar ticket nuevo a Celery SOLO UNA VEZ
# -----------------------------------------------------------
@receiver(post_save, sender=Ticket)
def process_ticket(sender, instance, created, **kwargs):
    """
    Enviar automáticamente ticket nuevo a Celery (solo clasificación).
    El churn se calcula en tasks.py para evitar dobles llamados.
    """
    if created:
        from .tasks import classify_ticket_task
        classify_ticket_task.delay(instance.id)
