
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.caja.models import Caja
from apps.inventario.models import Articulos, Inventario
from .models import Servicio
from .forms import ServicioForm

@login_required(login_url='login') #redirect when user is not logged in
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

        # Restar del inventario elarticulo que se incluyó
        if servicio.articulo:
            articulo_servicio = Articulos.objects.get(id=servicio.articulo.id)
            inventario = Inventario.objects.get(articulo=articulo_servicio)
            inventario.existencias = (inventario.existencias-servicio.articulos_cantidad)
            inventario.save()

        messages.success(request, "Se realizó el servicio")
        return redirect('servicios_realizados')
    else:
        form = ServicioForm()
    return render(request, 'servicios/servicio_form.html', {'form': form})
