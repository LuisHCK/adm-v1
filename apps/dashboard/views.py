
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.ventas.models import Venta
from apps.inventario.models import Inventario
from apps.caja.models import Caja
from apps.servicios.models import Servicio
from apps.servicios.views import realizar_servicio as realizar_servicio
from .forms import VentaForm
from apps.servicios.forms import ServicioForm

@login_required(login_url='login') #redirect when user is not logged in


# Create your views here.


def inicio(request):
    """Retorna la pagina de inicio"""
    venta = Venta.objects.all().order_by('-fecha_venta')[:5]
    servicios = Servicio.objects.all().order_by('-fecha_servicio')[:5]
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

            # Guardar en Caja
            caja = Caja.objects.last()
            if caja:
                caja.saldo += venta.total
                caja.save()
            else:
                Caja.objects.create(saldo=venta.total, usuario=request.user)

        return redirect('inicio')
    else:
        form = VentaForm()
        form2 = ServicioForm()
    return render(request, 'dashboard/dashboard.html',
                  {'venta': venta, 'caja': caja, 'count_servicios': count_servicios,
                   'servicios': servicios, 'form_venta': form, 'form_servicio': form2})
