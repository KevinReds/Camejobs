from django.apps import AppConfig # Importa la clase base para configuraciones de aplicaciones


class TicketsConfig(AppConfig): # Configuración específica para la app 'tickets'
    default_auto_field = 'django.db.models.BigAutoField' # Usa BigAutoField como campo automático por defecto
    name = 'tickets' # Nombre de la aplicación
