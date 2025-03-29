# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm
from django.contrib import messages

@login_required
def crear_ticket(request): 
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.usuario = request.user  # Asigna automáticamente el usuario
            ticket.save()
            
            # Limpiamos mensajes antes de agregar uno nuevo
            storage = messages.get_messages(request)
            storage.used = True
            
            messages.success(request, '¡Ticket creado exitosamente!')
            return redirect('tickets:listar_tickets')
    else:
        form = TicketForm()
        

    # Limpiamos mensajes antes de agregar uno nuevo
    storage = messages.get_messages(request)
    storage.used = True
   
    return render(request, 'tickets/crear_ticket.html', {'form': form})

@login_required
def listar_tickets(request):
    
    tickets = Ticket.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'tickets/listar_tickets.html', {'tickets': tickets})

@login_required
def editar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, usuario=request.user)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            
            # Limpiamos mensajes antes de agregar uno nuevo
            storage = messages.get_messages(request)
            storage.used = True
            
            messages.success(request, 'Ticket actualizado exitosamente.')
            return redirect('tickets:listar_tickets')
    else:
        form = TicketForm(instance=ticket)  
    
    return render(request, 'tickets/editar_ticket.html', {'form': form})

@login_required
def eliminar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, usuario=request.user)
    ticket.delete()
    
    # Limpiamos mensajes antes de agregar uno nuevo
    storage = messages.get_messages(request)
    storage.used = True
    messages.success(request, 'Ticket eliminado exitosamente.')
    

    
    return redirect('tickets:listar_tickets')