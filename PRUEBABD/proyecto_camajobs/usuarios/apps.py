from django.apps import AppConfig # Importa la clase base para configuraciones de aplicaciones


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' # Tipo de campo automático por defecto (para primary keys)
    name = 'usuarios' # Nombre de la aplicación
