
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.caja.models import Caja
from apps.inventario.models import Inventory
from apps.ventas.models import Sale
from apps.cloud.views import send_to_api

from .forms import VentaForm


# Create your views here.


@login_required(login_url='login')  # redirect when user is not logged in
def ventas(request):
    """Retorna la pagina de inicio"""
    venta = Sale.objects.all().order_by('-created_at')
    return render(request, 'ventas/venta.html', {'venta': venta, 'form_venta': VentaForm})


def realizar_venta(request):
    """Realiza la venta de un artículo"""
    # Obtener las stocks actuales del producto
    venta = object
    if request.method == "POST":
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            # Registra el user que realiza la venta
            venta.user = request.user
            # Calcula el total de la venta
            venta.total = (venta.product.sale_price * venta.quantity)
            venta.save()

        # Restar producto del inventario
        inventario = Inventory.objects.get(product=venta.product)

        # Si la quantity es nula o menor a uno se le asigna un 1
        if venta.quantity < 1:
            venta.quantity = 1

        inventario.stocks = (inventario.stocks - venta.quantity)
        inventario.save()

        # Guardar en Caja
        caja = Caja.objects.last()
        if caja:
            caja.saldo = (caja.saldo + venta.total)
            caja.save()
        else:
            Caja.objects.create(saldo=venta.total, user=request.user)

        # Enviar los datos a la api
        data_caja = {
            'total': str(caja.saldo),
            'date_open': str(caja.fecha_apertura),
            'date_close': str(caja.fecha_cierre)
        }
        send_to_api(data_caja, 'cashes')

        # Guardar datos de venta en la API
        data = {"product": str(venta.product),
                "price": str(venta.product.sale_price),
                "quantity": str(venta.quantity),
                "seller": str(venta.user)}
        send_to_api(data, 'sales')

        return redirect('ventas')

    else:
        form = VentaForm()
    return render(request, 'ventas/nueva.html', {'form': form})
