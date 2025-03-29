# Importación de módulos necesarios de Django
from django import forms # Para crear formularios personalizados
from django.contrib.auth.forms import UserCreationForm # Formulario base para creación de usuarios
from django.contrib.auth.models import User # Modelo de usuario por defecto de Django
from .models import Persona, Empresa, FormacionAcademica, ExperienciaLaboral, CalificacionPersona, CalificacionEmpresa # Importación de modelos locales
# VALIDACIÓN - Importaciones para manejo de autenticación y validación
from django.contrib.auth.forms import AuthenticationForm # Formulario base para login
from django.contrib import messages # Para mostrar mensajes al usuario
from django.core.exceptions import ValidationError # Para manejar errores de validación
from django.contrib.auth import authenticate # Para autenticar usuarios
from django.utils.translation import gettext_lazy as _ # Para internacionalización

# Formulario de registro para Personas 
class RegistroPersonaForm(UserCreationForm):
    # Campos adicionales al formulario base de UserCreationForm
    cedula = forms.CharField(max_length=15, label="Cédula") # Campo para número de cédula
    nombre_completo = forms.CharField(max_length=100, label="Nombre Completo") # Nombre completo
    telefono = forms.CharField(max_length=15, label="Teléfono") # Número telefónico
    profesion = forms.CharField(max_length=100, label="Profesión") # Profesión u oficio
    direccion = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ej: Calle 123 #45-67'}), label="Dirección") # Campo de dirección con placeholder de ejemplo
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Fecha de Nacimiento")  # Campo de fecha con widget tipo date para selección en calendario
    genero = forms.ChoiceField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], label="Género") # Selección de género con opciones predefinidas
    habilidades = forms.CharField(widget=forms.Textarea, label="Habilidades") # Campo de texto largo para habilidades
    email = forms.EmailField(label="Correo Electrónico") # Email con validación de formato
    ubicacion = forms.CharField(max_length=100, label="Ubicación") # Ubicación geográfica
    foto_perfil = forms.ImageField(required=False, label="Foto de Perfil")  # Imagen opcional

    # Método para guardar el formulario
    def save(self, commit=True):
        # Validar el formulario antes de guardar
        if not self.is_valid():
            raise ValidationError("El formulario no es válido.")
        
        # Guardado del usuario base
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Sincroniza el email con el User
        user.is_active = False  # Usuario inactivo hasta confirmar correo
        
        if commit:
            user.save() # Guardar el User
            # Crear el perfil Persona
            Persona.objects.create(
                usuario=user,
                cedula=self.cleaned_data['cedula'],
                nombre_completo=self.cleaned_data['nombre_completo'],
                telefono=self.cleaned_data['telefono'],
                profesion=self.cleaned_data['profesion'],
                direccion=self.cleaned_data['direccion'],
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
                genero=self.cleaned_data['genero'],
                habilidades=self.cleaned_data['habilidades'],
                email=self.cleaned_data['email'],
                ubicacion=self.cleaned_data['ubicacion'],
                foto_perfil=self.cleaned_data['foto_perfil']
            )
        return user

    # Configuración del Meta para el formulario
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'cedula', 'nombre_completo', 'telefono', 'profesion', 'direccion', 'fecha_nacimiento', 'genero', 'habilidades', 'email', 'ubicacion','foto_perfil']

# Formulario de registro para Empresas
class RegistroEmpresaForm(UserCreationForm):
    nit = forms.CharField(max_length=20, label="NIT")  # Número de identificación tributaria
    razon_social = forms.CharField(max_length=100, label="Razón Social") # Nombre legal
    telefono = forms.CharField(max_length=15, label="Teléfono")  # Teléfono de contacto
    eslogan = forms.CharField(max_length=200, label="Eslogan", required=False) # Eslogan opcional
    direccion = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ej: Avenida Principal #100-23'}), label="Dirección")  # Campo de dirección con placeholder
    sitio_web = forms.URLField(required=False, label="Sitio Web") # URL opcional
    descripcion = forms.CharField(widget=forms.Textarea, label="Descripción") # Descripción de la empresa
    email = forms.EmailField(label="Correo Electrónico") # Email corporativo
    ubicacion = forms.CharField(max_length=100, label="Ubicación") # Ubicación geográfica
    logo = forms.ImageField(required=False, label="Logo") # Logo opcional
     
     # Método para guardar el formulario 
    def save(self, commit=True):
        
        # Validar el formulario antes de guardar
        if not self.is_valid():
            raise ValidationError("El formulario no es válido.")

        # Guardado del usuario base
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Sincroniza el email con el User
        user.is_active = False  # Usuario inactivo hasta confirmar correo
        
        if commit:
            user.save() # Guardar el User
            # Crear el perfil Empresa
            Empresa.objects.create(
                usuario=user,
                nit=self.cleaned_data['nit'],
                razon_social=self.cleaned_data['razon_social'],
                telefono=self.cleaned_data['telefono'],
                eslogan=self.cleaned_data['eslogan'],
                direccion=self.cleaned_data['direccion'],
                sitio_web=self.cleaned_data['sitio_web'],
                descripcion=self.cleaned_data['descripcion'],
                email=self.cleaned_data['email'],
                ubicacion=self.cleaned_data['ubicacion'],
                logo=self.cleaned_data['logo']
            ) 
        return user

     # Configuración del Meta para el formulario
    class Meta:
        model = User  # Modelo base que extiende
        fields = ['username', 'password1', 'password2', 'nit', 'razon_social', 'telefono', 'eslogan', 'direccion', 'sitio_web', 'descripcion', 'email', 'ubicacion', 'logo']
        
# Formulario para Formación Académica (relacionado con Persona)
class FormacionAcademicaForm(forms.ModelForm):
    class Meta:
        model = FormacionAcademica # Modelo asociado
        fields = ['nivel_educativo', 'institucion', 'titulo_obtenido', 'fecha_inicio', 'fecha_fin', 'en_progreso']
         # Widgets personalizados para campos de fecha
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }
        
# Formulario para Experiencia Laboral (relacionado con Persona)
class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral # Modelo asociado
        fields = ['nombre_empresa', 'cargo', 'fecha_inicio', 'fecha_fin', 'descripcion', 'en_progreso']
        # Widgets personalizados para campos de fecha
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }
 
# Formulario para calificar Personas (hecho por Empresas)  
class CalificacionPersonaForm(forms.ModelForm):
    class Meta:
        model = CalificacionPersona # Modelo asociado
        fields = ['puntuacion', 'comentario']
        # Widgets personalizados
        widgets = {
            'puntuacion': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comentario': forms.Textarea(attrs={'rows': 4}),
        }
        
# Formulario para calificar Empresas (hecho por Personas)
class CalificacionEmpresaForm(forms.ModelForm):
    class Meta:
        model = CalificacionEmpresa  # Modelo asociado
        fields = ['puntuacion', 'comentario']
        # Widgets personalizados
        widgets = {
            'puntuacion': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comentario': forms.Textarea(attrs={'rows': 4}),
        }

# Formulario personalizado de autenticación
class CustomAuthenticationForm(AuthenticationForm):
    # Método para limpieza y validación de datos
    def clean(self):
        username = self.cleaned_data.get('username') # Obtener username
        password = self.cleaned_data.get('password') # Obtener password

        if username is not None and password:
            # Intentar autenticar al usuario
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )
            
            # Verifica si el usuario existe pero no está activo
            if self.user_cache is None:
                try:
                    user_temp = User.objects.get(username=username)
                    if not user_temp.is_active:
                        raise ValidationError(
                            _("¡Cuenta no verificada! Revisa tu correo para activarla."),
                            code='inactive_account',
                        )
                except User.DoesNotExist:
                    pass # Usuario no existe

                
                raise self.get_invalid_login_error() # Lanzar error de login inválido
            
            self.confirm_login_allowed(self.user_cache) # Confirmar que el usuario puede loguearse

        return self.cleaned_data  # Retornar datos limpios     

# Formulario para edición de Perfil de Persona    
class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona  # Modelo asociado
        fields = [
            'nombre_completo', 'profesion', 'telefono', 'direccion',
            'email', 'ubicacion',
            'habilidades', 'perfil_laboral', 'foto_perfil'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

# Formulario para edición de Perfil de Empresa
class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'nit', 'razon_social', 'eslogan', 'telefono', 'direccion',
            'email', 'sitio_web', 'descripcion',
            'ubicacion', 'logo'
        ]