
from django.shortcuts import render, redirect
from apps.ventas.models import Venta
from apps.inventario.models import Inventario
from .forms import VentaForm

# Create your views here.


def ventas(request):
    """Retorna la pagina de inicio"""
    venta = Venta.objects.all()
    return render(request, 'ventas/venta.html', {'venta': venta})


def realizar_venta(request):
    """Realiza la venta de un artículo"""
    if request.method == "POST":
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            # Registra el usuario que realiza la venta
            venta.usuario = request.user
            # Calcula el total de la venta
            venta.total = venta.articulo.precio_venta * venta.cantidad
            venta.save()
        # Restar producto del inventario
        inventario = Inventario.objects.get(articulo=venta.articulo)
        inventario.existencias = (inventario.existencias-venta.cantidad)
        inventario.save()
        return redirect('ventas')
    else:
        form = VentaForm()
    return render(request, 'ventas/nueva.html', {'form': form})
