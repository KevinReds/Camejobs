# Importación de módulos necesarios de Django
from django.db import models  # Para definir modelos de base de datos
from django.contrib.auth.models import User  # Modelo de usuario por defecto de Django
from django.core.validators import MinValueValidator, MaxValueValidator  # Validadores para campos numéricos

# Modelo que representa una Persona 
class Persona(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE) # Relación uno-a-uno con el modelo User de Django (sistema de autenticación)
    nombre_completo = models.CharField(max_length=100, verbose_name="Nombre Completo")  # Nombre completo de la persona (máximo 100 caracteres)
    cedula = models.CharField(max_length=15, unique=True, verbose_name="Cédula")  # Número de identificación único (cédula)
    profesion = models.CharField(max_length=100, verbose_name="Profesión") # Profesión u ocupación principal
    telefono = models.CharField(max_length=15, verbose_name="Teléfono") # Número de teléfono de contacto
    direccion = models.CharField(max_length=200, verbose_name="Dirección") # Dirección física de residencia
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento") # Fecha de nacimiento de la persona
    genero = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], verbose_name="Género") # Género con opciones predefinidas (M, F, O)
    email = models.EmailField(verbose_name="Correo Electrónico") # Correo electrónico (validado como formato email)
    ubicacion = models.CharField(max_length=100, verbose_name="Ubicación") # Ubicación geográfica
    habilidades = models.TextField(verbose_name="Habilidades") # Descripción de habilidades (texto largo)
    perfil_laboral = models.TextField(verbose_name="Perfil Laboral") # Perfil profesional/resumen laboral
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True, verbose_name="Foto de Perfil") # Imagen de perfil

     # Método para representación string del objeto
    def __str__(self):  
        return f"{self.usuario.username} - {self.cedula}"
    
# Modelo que representa una Empresa
class Empresa(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE) # Relación uno-a-uno con el modelo User de Django
    nit = models.CharField(max_length=20, unique=True, verbose_name="NIT")  # Número de Identificación Tributaria (único)
    razon_social = models.CharField(max_length=100, verbose_name="Razón Social") # Nombre legal de la empresa
    eslogan = models.CharField(max_length=200, verbose_name="Eslogan", blank=True)  # Eslogan o frase representativa (opcional)
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")  # Teléfono de contacto
    direccion = models.CharField(max_length=200, verbose_name="Dirección")  # Dirección física principal
    email = models.EmailField(verbose_name="Correo Electrónico") # Correo electrónico corporativo
    sitio_web = models.URLField(blank=True, null=True, verbose_name="Sitio Web") # URL del sitio web (opcional)
    descripcion = models.TextField(verbose_name="Descripción") # Descripción general de la empresa
    ubicacion = models.CharField(max_length=100, verbose_name="Ubicación") # Ubicación geográfica principal
    logo = models.ImageField(upload_to='logos_empresa/', null=True, blank=True, verbose_name="Logo") # Logo de la empresa

     # Método para representación string del objeto
    def __str__(self): 
        return f"{self.razon_social} - {self.nit}"

# Modelo para el historial académico de una Persona    
class FormacionAcademica(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name="Persona") # Relación muchos-a-uno con Persona (una persona puede tener múltiples formaciones)
    # Nivel educativo con opciones predefinidas
    nivel_educativo = models.CharField( 
        max_length=50,
        choices=[
            ('Bachiller', 'Bachiller'),
            ('Técnico', 'Técnico'),
            ('Tecnólogo', 'Tecnólogo'),
            ('Pregrado', 'Pregrado'),
            ('Posgrado', 'Posgrado'),
            ('Curso', 'Curso'),
            ('Otro', 'Otro'),
        ],
        verbose_name="Nivel Educativo"
    )
    institucion = models.CharField(max_length=100, verbose_name="Institución") # Institución educativa donde se realizó la formación
    titulo_obtenido = models.CharField(max_length=100, verbose_name="Título Obtenido") # Título obtenido
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio") # Fecha de inicio de los estudios
    fecha_fin = models.DateField(verbose_name="Fecha de Fin", null=True, blank=True)  # Fecha de finalización (puede ser nulo si está en progreso)
    en_progreso = models.BooleanField(default=False, verbose_name="En Progreso")  #indica si la formación está en curso

    # Método para representación string del objeto
    def __str__(self):
        return f"{self.persona.usuario.username} - {self.titulo_obtenido} ({self.nivel_educativo})"

# Modelo para el historial laboral de una Persona    
class ExperienciaLaboral(models.Model): 
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name="Persona") # Relación muchos-a-uno con Persona (una persona puede tener múltiples experiencias)
    nombre_empresa = models.CharField(max_length=100, verbose_name="Nombre de la Empresa") # Nombre de la empresa donde trabajó
    cargo = models.CharField(max_length=100, verbose_name="Cargo")  # Cargo o posición ocupada
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio") # Fecha de inicio del trabajo
    fecha_fin = models.DateField(verbose_name="Fecha de Fin", null=True, blank=True)  # Fecha de finalización (puede ser nulo si está en progreso)
    descripcion = models.TextField(verbose_name="Descripción") # Descripción de responsabilidades y logros
    en_progreso = models.BooleanField(default=False, verbose_name="En Progreso") # Bandera que indica si la experiencia está en curso

    # Método para representación string del objeto
    def __str__(self):
        return f"{self.persona.usuario.username} - {self.cargo} en {self.nombre_empresa}"
    
# Modelo para calificaciones que las Empresas hacen a las Personas
class CalificacionPersona(models.Model):
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, related_name='calificaciones_hechas') # Empresa que realiza la calificación
    persona = models.ForeignKey('Persona', on_delete=models.CASCADE, related_name='calificaciones_recibidas') # Persona que recibe la calificación
    puntuacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # Calificación de 1 a 5
    comentario = models.TextField(blank=True, null=True)  # Opcional: Comentario sobre la calificación
    fecha = models.DateTimeField(auto_now_add=True) # Fecha automática de creación (se establece al crear el registro)

    # Método para representación string del objeto
    def __str__(self):
        return f"{self.empresa.razon_social} -> {self.persona.nombre_completo}: {self.puntuacion} estrellas"

# Modelo para calificaciones que las Personas hacen a las Empresas
class CalificacionEmpresa(models.Model):
    persona = models.ForeignKey('Persona', on_delete=models.CASCADE, related_name='calificaciones_hechas') # Persona que realiza la calificación
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, related_name='calificaciones_recibidas') # Empresa que recibe la calificación
    puntuacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # Calificación de 1 a 5
    comentario = models.TextField(blank=True, null=True)  # Opcional: Comentario sobre la calificación
    fecha = models.DateTimeField(auto_now_add=True) # Fecha automática de creación (se establece al crear el registro)

    # Método para representación string del objeto
    def __str__(self):
        return f"{self.persona.nombre_completo} -> {self.empresa.razon_social}: {self.puntuacion} estrellas"    