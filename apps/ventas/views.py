
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.ventas.models import Venta
from apps.inventario.models import Inventario
from apps.caja.models import Caja
from .forms import VentaForm

# Create your views here.
@login_required(login_url='login') #redirect when user is not logged in

def ventas(request):
    """Retorna la pagina de inicio"""
    venta = Venta.objects.all().order_by('-fecha_venta')
    return render(request, 'ventas/venta.html', {'venta': venta})


def realizar_venta(request):
    """Realiza la venta de un artículo"""
    #Obtener las existencias actuales del producto
    if request.method == "POST":
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            # Registra el usuario que realiza la venta
            venta.usuario = request.user
            # Calcula el total de la venta
            venta.total = (venta.articulo.precio_venta * venta.cantidad)
            venta.save()

        # Restar producto del inventario
        inventario = Inventario.objects.get(articulo=venta.articulo)

        # Si la cantidad es nula o menor a uno se le asigna un 1
        if venta.cantidad < 1:
            venta.cantidad = 1

        inventario.existencias = (inventario.existencias - venta.cantidad)
        inventario.save()

        # Guardar en Caja
        caja = Caja.objects.last()
        if caja:
            caja.saldo = (caja.saldo + venta.total)
            caja.save()
        else:
            Caja.objects.create(saldo=venta.total, usuario=request.user)

        return redirect('ventas')
    else:
        form = VentaForm()
    return render(request, 'ventas/nueva.html', {'form': form})
