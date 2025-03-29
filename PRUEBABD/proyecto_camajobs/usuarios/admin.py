# Importación del módulo de administración de Django
from django.contrib import admin
# Importación de los modelos locales que se registrarán en el admin
from .models import Persona, Empresa, FormacionAcademica, ExperienciaLaboral
# Register your models here.

# Configuración del panel de administración para el modelo Persona
@admin.register(Persona) # Registra el modelo Persona en el admin
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cedula', 'email', 'habilidades') # Campos visibles en la lista

# Configuración del panel de administración para el modelo Empresa
@admin.register(Empresa)  # Registra el modelo Empresa en el admin
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'razon_social', 'nit', 'email') # Campos visibles en la lista

# Configuración del panel de administración para el modelo FormacionAcademica
@admin.register(FormacionAcademica)
class FormacionAcademicaAdmin(admin.ModelAdmin):
    list_display = ('persona', 'nivel_educativo', 'titulo_obtenido', 'institucion')

# Configuración del panel de administración para el modelo ExperienciaLaboral
@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ('persona', 'nombre_empresa', 'cargo', 'fecha_inicio', 'fecha_fin')