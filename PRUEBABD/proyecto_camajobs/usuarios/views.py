from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login
from .forms import PersonaForm, EmpresaForm
from django.forms import modelformset_factory
from .forms import (
    RegistroPersonaForm, RegistroEmpresaForm, 
    CalificacionPersona, CalificacionEmpresa,
    FormacionAcademicaForm, ExperienciaLaboralForm, 
    CalificacionPersonaForm, CalificacionEmpresaForm
)
from .models import Persona, Empresa, FormacionAcademica, ExperienciaLaboral
from django.contrib.auth.decorators import login_required
from usuarios.models import Persona, Empresa
from ofertas.models import Oferta, Postulacion
from django.contrib import messages
from tickets.models import Ticket
from django.db.models import Avg, Count
from django.views import View
from django.contrib.auth.views import LoginView

#neceesario para validación
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Vista para la página principal
def pagina_principal(request):
    return render(request, 'usuarios/paginaPrincipal.html')

# Vista de inicio de sesión personalizada
class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'  # Cambia esto al template de inicio de sesión

# Vista de inicio (opcional)
def inicio(request):
    return render(request, 'usuarios/inicio.html')

# Registro de persona
def registro_persona(request):
    if request.method == 'POST':
        form = RegistroPersonaForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                           
                # Generar enlace de confirmación
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                confirm_link = f"{request.scheme}://{request.get_host()}/usuarios/confirmar-email/{uid}/{token}/"
                
                # Enviar correo
                send_mail(
                    'Confirma tu correo electrónico',
                    f'Haz clic aquí para confirmar tu cuenta: {confirm_link}',
                    'no-reply@camajobs.com',
                    [user.email],
                    fail_silently=False,
                )
                return redirect('confirmacion-enviada')
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = RegistroPersonaForm()
    return render(request, 'usuarios/registro_persona.html', {'form': form})

# Registro de empresa
def registro_empresa(request):
    if request.method == 'POST':
        form = RegistroEmpresaForm(request.POST, request.FILES)
        if form.is_valid():           
            try:               
                user = form.save()
                           
                # Generar enlace de confirmación (mismo código que en registro_persona)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                current_site = get_current_site(request).domain
                confirm_link = f"{request.scheme}://{request.get_host()}/usuarios/confirmar-email/{uid}/{token}/"

                # Enviar correo
                send_mail(
                    'Confirma tu correo electrónico',
                    f'Haz clic aquí para confirmar tu cuenta: {confirm_link}',
                    'no-reply@camajobs.com',
                    [user.email],
                    fail_silently=False,
                )
                return redirect('confirmacion-enviada')
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = RegistroEmpresaForm()
    return render(request, 'usuarios/registro_empresa.html', {'form': form})

# Vista de postulaciones
@login_required
def postulaciones(request):
    usuario = request.user
    ofertas_activas = Oferta.objects.filter(activa=True)
    context = {
        'usuario': usuario,
        'ofertas': ofertas_activas,
    }

    if hasattr(usuario, 'persona'):
        context['tipo'] = 'persona'
        context['nombre'] = usuario.persona.nombre_completo
        
        # Obtener todas las postulaciones de la persona
        postulaciones = Postulacion.objects.filter(trabajador=usuario.persona)
        context['postulaciones'] = postulaciones
        
        # Obtener ofertas en las que la persona ha sido aceptada
        ofertas_aceptadas = postulaciones.filter(estado="Aprobado").values_list('oferta_id', flat=True)
        context['ofertas_aceptadas'] = list(ofertas_aceptadas)  # Convertir a lista
        
        #diccionario para acceder rápidamente a las postulaciones por oferta
        postulaciones_dict = {p.oferta.id: p for p in postulaciones}
        context['postulaciones_dict'] = postulaciones_dict
        
        #Asignar la postulación a cada oferta si existe
        for oferta in ofertas_activas:
            oferta.postulacion = postulaciones_dict.get(oferta.id, None)
        
        context['empresas_calificadas'] = Empresa.objects.filter(
            calificaciones_recibidas__persona=usuario.persona
        ).annotate(
            promedio_calificaciones=Avg('calificaciones_recibidas__puntuacion'),
            cantidad_calificaciones=Count('calificaciones_recibidas')
        ).distinct()

    elif hasattr(usuario, 'empresa'):
        context['tipo'] = 'empresa'
        context['nombre'] = usuario.empresa.razon_social
        ofertas_empresa = Oferta.objects.filter(empresa=usuario.empresa, activa=True)
        context['ofertas_empresa'] = ofertas_empresa
        context['personas_calificadas'] = Persona.objects.filter(
            calificaciones_recibidas__empresa=usuario.empresa
        ).annotate(
            promedio_calificaciones=Avg('calificaciones_recibidas__puntuacion'),
            cantidad_calificaciones=Count('calificaciones_recibidas')
        ).distinct()

    return render(request, 'usuarios/postulaciones.html', context)

# Perfil de persona
@login_required
def perfil_persona(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)
    formaciones = FormacionAcademica.objects.filter(persona=persona)
    experiencias = ExperienciaLaboral.objects.filter(persona=persona)
    tickets = Ticket.objects.filter(usuario=request.user)

    personas_calificadas = Persona.objects.filter(
        calificaciones_recibidas__persona=persona
    ).annotate(
        promedio_calificaciones=Avg('calificaciones_recibidas__puntuacion'),
        cantidad_calificaciones=Count('calificaciones_recibidas')
    ).distinct()

    return render(request, 'usuarios/perfil_persona.html', {
        'persona': persona,
        'formaciones': formaciones,
        'experiencias': experiencias,
        'tickets': tickets,
        'personas_calificadas': personas_calificadas,
    })

@login_required
def modificar_perfil(request):
    persona = request.user.persona
    if request.method == 'POST':
        persona_form = PersonaForm(request.POST, request.FILES, instance=persona)
        if persona_form.is_valid():
            persona_form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('perfil_persona')
    else:
        persona_form = PersonaForm(instance=persona)
    return render(request, 'usuarios/modificar_perfil.html', {
        'persona_form': persona_form,
    })

# Perfil de empresa
@login_required
def perfil_empresa(request, empresa_id=None):
    if empresa_id:
        empresa = get_object_or_404(Empresa, id=empresa_id)
    else:
        empresa = get_object_or_404(Empresa, usuario=request.user)

    tickets = Ticket.objects.filter(usuario=request.user)

    empresas_calificadas = Empresa.objects.filter(
        calificaciones_recibidas__empresa=empresa
    ).annotate(
        promedio_calificaciones=Avg('calificaciones_recibidas__puntuacion'),
        cantidad_calificaciones=Count('calificaciones_recibidas')
    ).distinct()

    return render(request, 'usuarios/perfil_empresa.html', {
        'empresa': empresa,
        'tickets': tickets,
        'empresas_calificadas': empresas_calificadas,
    })

@login_required
def modificar_empresa(request):
    empresa = request.user.empresa
    if request.method == 'POST':
        empresa_form = EmpresaForm(request.POST, request.FILES, instance=empresa)
        if empresa_form.is_valid():
            empresa_form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('perfil_empresa')
    else:
        empresa_form = EmpresaForm(instance=empresa)
    return render(request, 'usuarios/modificar_empresa.html', {
        'empresa_form': empresa_form,
    })

# Funciones adicionales para la formación y experiencia académica
@login_required
def agregar_formacion(request):
    persona = get_object_or_404(Persona, usuario=request.user)
    if request.method == 'POST':
        form = FormacionAcademicaForm(request.POST)
        if form.is_valid():
            formacion = form.save(commit=False)
            formacion.persona = persona
            formacion.save()
            messages.success(request, 'Formación académica agregada correctamente.')
            return redirect('perfil_persona')
    else:
        form = FormacionAcademicaForm()

    return render(request, 'usuarios/agregar_formacion.html', {'form': form})

@login_required
def editar_formacion(request, formacion_id):
    formacion = get_object_or_404(FormacionAcademica, id=formacion_id, persona__usuario=request.user)
    if request.method == 'POST':
        form = FormacionAcademicaForm(request.POST, instance=formacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Formación académica actualizada correctamente.')
            return redirect('perfil_persona')
    else:
        form = FormacionAcademicaForm(instance=formacion)

    return render(request, 'usuarios/editar_formacion.html', {'form': form})

@login_required
def eliminar_formacion(request, formacion_id):
    formacion = get_object_or_404(FormacionAcademica, id=formacion_id, persona__usuario=request.user)
    formacion.delete()
    messages.success(request, 'Formación académica eliminada correctamente.')
    return redirect('perfil_persona')

# Vistas para la experiencia laboral
@login_required
def agregar_experiencia(request):
    persona = get_object_or_404(Persona, usuario=request.user)
    if request.method == 'POST':
        form = ExperienciaLaboralForm(request.POST)
        if form.is_valid():
            experiencia = form.save(commit=False)
            experiencia.persona = persona
            experiencia.save()
            messages.success(request, 'Experiencia laboral agregada correctamente.')
            return redirect('perfil_persona')
    else:
        form = ExperienciaLaboralForm()

    return render(request, 'usuarios/agregar_experiencia.html', {'form': form})

@login_required
def editar_experiencia(request, experiencia_id):
    experiencia = get_object_or_404(ExperienciaLaboral, id=experiencia_id, persona__usuario=request.user)
    if request.method == 'POST':
        form = ExperienciaLaboralForm(request.POST, instance=experiencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experiencia laboral actualizada correctamente.')
            return redirect('perfil_persona')
    else:
        form = ExperienciaLaboralForm(instance=experiencia)

    return render(request, 'usuarios/editar_experiencia.html', {'form': form})

@login_required
def eliminar_experiencia(request, experiencia_id):
    experiencia = get_object_or_404(ExperienciaLaboral, id=experiencia_id, persona__usuario=request.user)
    experiencia.delete()
    messages.success(request, 'Experiencia laboral eliminada correctamente.')
    return redirect('perfil_persona')

# Vistas de calificación
@login_required
def calificar_persona(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)
    empresa = get_object_or_404(Empresa, usuario=request.user)

    if request.method == 'POST':
        form = CalificacionPersonaForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.empresa = empresa
            calificacion.persona = persona
            calificacion.save()
            messages.success(request, 'Calificación enviada exitosamente.')
            return redirect('perfil_persona', persona_id=persona.id)
    else:
        form = CalificacionPersonaForm()

    return render(request, 'usuarios/calificar_persona.html', {'form': form, 'persona': persona})

@login_required
def calificar_empresa(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    persona = get_object_or_404(Persona, usuario=request.user)

    if request.method == 'POST':
        form = CalificacionEmpresaForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.persona = persona
            calificacion.empresa = empresa
            calificacion.save()
            messages.success(request, 'Calificación enviada exitosamente.')
            return redirect('perfil_empresa', empresa_id=empresa.id)
    else:
        form = CalificacionEmpresaForm()

    return render(request, 'usuarios/calificar_empresa.html', {'form': form, 'empresa': empresa})

#Preguntas frecuentes
def faqs_pagina(request):
    return render(request, 'usuarios/faqs_pagina.html')

#Quienes somos
def quienes_somos(request):
    return render(request, 'usuarios/quienes_somos.html')

#Pagina de perfiles
@login_required
def busquedas_pagina(request):
    return render(request, 'usuarios/busquedas_pagina.html')

#confirmar correo
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login

def confirmar_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('postulaciones')
    else:
        return render(request, 'usuarios/enlace_invalido.html')
    
def confirmacion_enviada(request):
    return render(request, 'usuarios/confirmacion_enviada.html')

#Botones ocultos
def navbar_context(request):
    perfil_persona = hasattr(request.user, 'persona')
    perfil_empresa = hasattr(request.user, 'empresa')

    return {
        'perfil_persona': perfil_persona,
        'perfil_empresa': perfil_empresa,
    }

#Perfiles personas
def pagina_perfiles(request):
    personas = Persona.objects.all()

    ubicaciones = Persona.objects.values_list('ubicacion', flat=True).distinct()

    context = {
        'personas': personas,
        'ubicaciones': ubicaciones
    }

    return render(request, 'usuarios/pagina_perfiles.html', context)

def perfiles_empresas(request):
    empresas = Empresa.objects.all() 

    ubicaciones = Empresa.objects.values_list('ubicacion', flat=True).distinct()  # Ubicaciones únicas

    context = {
        'empresas': empresas,
        'ubicaciones': ubicaciones
    }

    return render(request, 'usuarios/perfiles_empresas.html', context)

#Acceder a perfiles por ID (Nit y cedula)
def redirigir_perfil(request, persona_id):
    persona = Persona.objects.filter(id=persona_id).first()
    
    if persona:
        return redirect(f'/usuarios/perfil/persona/{persona_id}/')

    empresa = Empresa.objects.filter(id=persona_id).first()
    
    if empresa:
        return redirect(reverse('perfil_empresa', kwargs={'empresa_id': persona_id}))

    return redirect('/usuarios/perfil/no-encontrado/')