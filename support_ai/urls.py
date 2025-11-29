from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from tickets.views import TicketViewSet, CustomerViewSet, AlertViewSet, dashboard_view

router = routers.DefaultRouter()
router.register('tickets', TicketViewSet)
router.register('customers', CustomerViewSet)
router.register('alerts', AlertViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # Dashboard
    path('', dashboard_view, name='dashboard_root'),  # acceso directo a /
    path('dashboard/', dashboard_view, name='dashboard'),  # acceso opcional a /dashboard/
]
