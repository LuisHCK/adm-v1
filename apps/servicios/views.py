from django.shortcuts import render, redirect
from .models import Servicio
from .forms import ServicioForm


# Create your views here.

def inicio(request):
    servicios = Servicio.objects.all()
    return render(request, 'servicios/servicios.html', {'servicios': servicios})

def realizar_servicio(request):
    """Realiza un registro del servicio realizado"""
    if request.method == "POST":
        form = ServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.usuario = request.user
            servicio.save()
        return redirect('inicio')
    else:
        form = ServicioForm()
    return render(request, 'servicios/servicio_form.html', {'form': form})
