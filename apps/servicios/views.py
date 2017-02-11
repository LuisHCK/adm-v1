
from django.shortcuts import render, redirect
from .models import Servicio
from .forms import ServicioForm
from apps.caja.models import Caja


# Create your views here.

def inicio(request):
    """Devuelve los servicios realizados"""
    servicios = Servicio.objects.all().order_by('-fecha_servicio')
    return render(request, 'servicios/servicios.html', {'servicios': servicios})

def realizar_servicio(request):
    """Realiza un registro del servicio realizado"""
    caja = Caja.objects.last()
    if request.method == "POST":
        form = ServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.usuario = request.user
            servicio.save()

        # Guardar en caja el monto del servicio
        caja.saldo = (caja.saldo + servicio.precio)
        caja.save()

        return redirect('servicios_realizados')
    else:
        form = ServicioForm()
    return render(request, 'servicios/servicio_form.html', {'form': form})
