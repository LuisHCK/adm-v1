from django.shortcuts import render, redirect
from apps.ventas.models import Venta
from apps.inventario.models import Inventario
from apps.caja.models import Caja
from apps.servicios.models import Servicio
from .forms import VentaForm


# Create your views here.


def inicio(request):
    """Retorna la pagina de inicio"""
    venta = Venta.objects.all().order_by('-fecha_venta')[:5]
    caja = Caja.objects.last()
    count_servicios = Servicio.objects.count()
    # Realiza la venta de un artículo
    if request.method == "POST":
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)

            # Registra el usuario que realiza la venta
            venta.usuario = request.user

            # Calcula el total de la venta
            venta.total = venta.articulo.precio_venta * venta.cantidad

            # Guardar la venta realizada
            venta.save()

            # Restar producto del inventario
            inventario = Inventario.objects.get(articulo=venta.articulo)
            inventario.existencias = (inventario.existencias - venta.cantidad)
            inventario.save()

        return redirect('inicio')
    else:
        form = VentaForm()
    return render(request, 'dashboard/dashboard.html', {'venta': venta, 'caja': caja, 'count_servicios': count_servicios, 'form_venta': form})
