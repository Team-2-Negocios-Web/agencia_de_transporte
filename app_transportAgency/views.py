from django.shortcuts import render
from datetime import *
from .models import *

def home(request):

    # Traer las rutas disponible 
    ticket = Ticket.objects.all()

    ctx = {
        'ticket' : ticket,
    }

    return render(request, 'transportAgency/home.html', ctx)