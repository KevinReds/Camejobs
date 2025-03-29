# Importación de módulos necesarios de Django
from django.urls import path  # Para definir patrones de URL
from . import views  # Importa las vistas definidas en el mismo directorio

# Namespace para las URLs de esta aplicación
# Permite referenciar estas URLs de forma única en todo el proyecto usando 'tickets:nombre_url'
app_name = 'tickets'

urlpatterns = [
    path('crear/', views.crear_ticket, name='crear_ticket'),
    path('listar/', views.listar_tickets, name='listar_tickets'),
    path('editar/<int:ticket_id>/', views.editar_ticket, name='editar_ticket'),
    path('eliminar/<int:ticket_id>/', views.eliminar_ticket, name='eliminar_ticket'),
    
]