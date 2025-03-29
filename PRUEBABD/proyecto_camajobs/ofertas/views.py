from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Oferta, Postulacion
from .forms import OfertaForm
from usuarios.models import Persona, CalificacionPersona
from django.utils import timezone
from django.contrib import messages
from usuarios.forms import CalificacionEmpresaForm , CalificacionPersonaForm
# Create your views here.

@login_required
def crear_oferta(request):
    if request.method == 'POST':
        form = OfertaForm(request.POST)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.empresa = request.user.empresa  # Asignar la empresa actual
            oferta.save()
            return redirect('postulaciones')
    else:
        form = OfertaForm()
    return render(request, 'ofertas/crear_oferta.html', {'form': form})

@login_required
def postular(request, oferta_id):
    oferta = get_object_or_404(Oferta, id=oferta_id)
    persona = request.user.persona  # Obtener el perfil de la persona

    # Crear la postulación si no existe
    Postulacion.objects.get_or_create(
        oferta=oferta,
        trabajador=persona,
        defaults={'estado': 'Pendiente'}
    )

    return redirect('postulaciones')

from django.shortcuts import render, get_object_or_404, redirect
from .models import Postulacion, Oferta
from django.contrib.auth.decorators import login_required

# Vista para listar postulaciones
@login_required
def listar_postulaciones(request, oferta_id):
    oferta = get_object_or_404(Oferta, id=oferta_id, empresa__usuario=request.user)
    postulaciones = Postulacion.objects.filter(oferta=oferta)
    return render(request, 'ofertas/listar_postulaciones.html', {'postulaciones': postulaciones, 'oferta': oferta})

# Vista para aceptar/rechazar postulaciones
@login_required
def gestionar_postulacion(request, postulacion_id, accion):
    postulacion = get_object_or_404(Postulacion, id=postulacion_id, oferta__empresa__usuario=request.user)
    if accion == 'aceptar':
        postulacion.estado = 'Aprobado'
        postulacion.fecha_contratacion = timezone.now().date()
    elif accion == 'rechazar':
        postulacion.estado = 'Rechazado'
    postulacion.save()
    return redirect('listar_postulaciones', oferta_id=postulacion.oferta.id)

@login_required
def ver_detalles_postulacion(request, postulacion_id):
    postulacion = get_object_or_404(Postulacion, id=postulacion_id, trabajador__usuario=request.user)
    context = {
        'postulacion': postulacion,
    }
    return render(request, 'ofertas/ver_detalles_postulacion.html', context)

@login_required
def calificar_empresa(request, postulacion_id):
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)
    empresa = postulacion.oferta.empresa
    persona = postulacion.trabajador

    if request.method == 'POST':
        form = CalificacionEmpresaForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.persona = persona
            calificacion.empresa = empresa
            calificacion.save()
            # Antes de agregar un nuevo mensaje, limpiamos cualquier mensaje previo
            storage = messages.get_messages(request)
            storage.used = True 
            messages.success(request, 'Calificación enviada exitosamente.')
            return redirect('perfil_empresa', empresa_id=empresa.id)
    else:
        form = CalificacionEmpresaForm()

    return render(request, 'ofertas/calificar_empresa.html', {'form': form, 'empresa': empresa})

@login_required
def calificar_persona(request, postulacion_id):
    postulacion = get_object_or_404(Postulacion, id=postulacion_id, oferta__empresa__usuario=request.user)
    persona = postulacion.trabajador
    empresa = postulacion.oferta.empresa
    

    if postulacion.estado != 'Aprobado':
        # Antes de agregar un nuevo mensaje, limpiamos cualquier mensaje previo
        storage = messages.get_messages(request)
        storage.used = True 
        messages.error(request, 'Solo puedes calificar a personas con postulaciones aprobadas.')
        return redirect('listar_postulaciones', oferta_id=postulacion.oferta.id)

    if request.method == 'POST':
        form = CalificacionPersonaForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.empresa = empresa
            calificacion.persona = persona
            calificacion.save()
            # Antes de agregar un nuevo mensaje, limpiamos cualquier mensaje previo
            storage = messages.get_messages(request)
            storage.used = True 
            messages.success(request, 'Calificación enviada exitosamente.')
            return redirect('listar_postulaciones', oferta_id=postulacion.oferta.id)
    else:
        form = CalificacionPersonaForm()

    return render(request, 'ofertas/calificar_persona.html', {'form': form, 'persona': persona, 'postulacion': postulacion})

#Función y elementos para ajustar la vista de las ofertas dependiendo de cuando se publicaron
from django.shortcuts import render
from .models import Oferta
from datetime import date 

#ofertas disponibles
def lista_ofertas (request):
    hoy = date.today()
    ofertas = Oferta.objects.filter(activa=True, fecha_cierre__gte=hoy).order_by('-fecha_publicacion')
    return render(request, 'ofertas/pagina_ofertas.html', {'ofertas': ofertas})

#Pagina ofertas
def pagina_ofertas(request):
    ofertas = Oferta.objects.filter(activa=True).order_by('-fecha_publicacion')
    ubicaciones = Oferta.objects.values_list('ubicacion', flat=True).distinct()
    empresas = Oferta.objects.values_list('empresa__razon_social', flat=True).distinct()

    
 
    
    context = {
        'ofertas': ofertas,
        'ubicaciones': ubicaciones,
        'empresas': empresas,
        
    }
    return render(request, 'ofertas/pagina_ofertas.html', context)