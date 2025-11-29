from rest_framework import serializers
from .models import Ticket, Customer, Alert

# Serializer de clientes
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'company', 'churn_risk']  # mejor no usar '__all__'

# Serializer de tickets
class TicketSerializer(serializers.ModelSerializer):
    # Para mostrar los datos del cliente en la API
    customer = CustomerSerializer(read_only=True)
    # Para crear/editar tickets usando solo el ID del cliente
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        write_only=True,
        source='customer'
    )

    class Meta:
        model = Ticket
        fields = [
            'id',
            'title',
            'description',
            'priority',
            'category',
            'customer',     # info completa para lectura
            'customer_id',  # solo para escritura
            'classified',
            'is_security',
            'created_at',
        ]
        read_only_fields = ('classified', 'is_security', 'created_at')

# Serializer de alertas
class AlertSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(read_only=True)  # opcional: incluir info del ticket
    class Meta:
        model = Alert
        fields = '__all__'

class AlertSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(read_only=True)  # para lectura
    ticket_id = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.all(),
        write_only=True,
        source='ticket'  # indica que se asigna al campo ticket del modelo
    )

    class Meta:
        model = Alert
        fields = [
            'id',
            'ticket',    # info completa para lectura
            'ticket_id', # solo para escritura
            'message',
            'level',
            'handled',
            'created_at',
        ]
        read_only_fields = ('handled', 'created_at')
