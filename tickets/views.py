# tickets/views.py

from rest_framework import viewsets
from django.shortcuts import render
from .models import Ticket, Customer, Alert
from .serializers import TicketSerializer, CustomerSerializer, AlertSerializer

# ----------------------------
# DRF API ViewSets
# ----------------------------
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    # Nota: NO lanzamos tareas aquí. El signal se encarga de eso.

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

# ----------------------------
# Dashboard Views (HTML)
# ----------------------------
def dashboard_view(request):
    tickets = Ticket.objects.all().order_by('-created_at')
    alerts = Alert.objects.filter(handled=False).order_by('-created_at')
    customers = Customer.objects.all()

    # Calcular métricas generales
    total_tickets = tickets.count()
    total_alerts = alerts.count()
    high_risk_customers = customers.filter(churn_risk__gte=0.7).count()

    context = {
        'tickets': tickets,
        'alerts': alerts,
        'customers': customers,
        'total_tickets': total_tickets,
        'total_alerts': total_alerts,
        'high_risk_customers': high_risk_customers,
    }

    return render(request, 'dashboard.html', context)
