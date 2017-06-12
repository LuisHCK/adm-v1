
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.formats import localize

from apps.caja.models import Caja
from apps.cloud.views import send_to_api
from apps.inventory.models import Inventory
from apps.servicios.forms import ServicioForm, TypeService
from apps.servicios.models import Service
from apps.ventas.models import Sale

from .forms import VentaForm


@login_required(login_url='login') #redirect when user is not logged in


# Create your views here.
def inicio(request):
    """Retorna la pagina de inicio"""
    venta = Sale.objects.all().order_by('-created_at')[:5]
    servicios = Service.objects.all().order_by('-created_at')[:5]
    caja = Caja.objects.last()
    count_servicios = Service.objects.count()
    # Realiza la venta de un artículo
    if request.method == "POST":
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)

            # Registra el user que realiza la venta
            venta.user = request.user

            # Calcula el total de la venta
            venta.total = venta.product.sale_price * venta.quantity

            # Guardar la venta realizada
            venta.save()

            # Restar producto del inventory
            inventory = Inventory.objects.get(product=venta.product)
            inventory.stocks = (inventory.stocks - venta.quantity)
            inventory.save()

            # Guardar en Caja
            caja = Caja.objects.last()
            if caja:
                caja.saldo += venta.total
                caja.save()
            else:
                Caja.objects.create(saldo=venta.total, user=request.user)

        return redirect('inicio')
    else:
        form = VentaForm()
        form2 = ServicioForm()
    return render(request, 'dashboard/dashboard.html',
                  {'venta': venta, 'caja': caja, 'count_servicios': count_servicios,
                   'servicios': servicios, 'form_venta': form, 'form_servicio': form2})

def venta_ajax(request):
    """Realiza la venta de un artículo"""
    # Obtener las stocks actuales del producto
    response_data = {}
    if request.method == "POST":
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            # Registra el user que realiza la venta
            venta.user = request.user
            # Calcula el total de la venta
            venta.total = (venta.product.sale_price * venta.quantity)
            venta.save()

        # Restar producto del inventory
        inventory = Inventory.objects.get(product=venta.product)

        # Si la quantity es nula o menor a uno se le asigna un 1
        if venta.quantity < 1:
            venta.quantity = 1

        inventory.stocks = (inventory.stocks - venta.quantity)
        inventory.save()

        # Guardar en Caja
        caja = Caja.objects.last()
        if caja:
            caja.saldo = (caja.saldo + venta.total)
            caja.save()
        else:
            Caja.objects.create(saldo=venta.total, user=request.user)

        response_data['result'] = "Se realizó la venta!"
        response_data['venta_id'] = str(venta.id)
        response_data['product'] = str(venta.product)
        response_data['quantity'] = str(venta.quantity)
        response_data['sale_price'] = str(venta.product.sale_price)
        response_data['purchase_price'] = str(venta.product.purchase_price)
        response_data['total'] = str(venta.total)
        response_data['vendedor'] = str(venta.user.username)
        response_data['created_at'] = str(localize(venta.created_at))

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

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        form = VentaForm()
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def servicio_ajax(request):
    """Realiza un registro del servicio realizado"""
    response_data = {}

    if request.method == "POST":
        form = ServicioForm(request.POST)

        if Caja.objects.count() > 0:
            if form.is_valid():
                servicio = form.save(commit=False)
                servicio.user = request.user

                # Asignar el price del servicio segun el tipo de servicio
                tiposervicio = TypeService.objects.get(
                    id=servicio.type_service.id)
                servicio.type_service = tiposervicio

                # Calcular el price en base a la quantity de producto

                # Si no se escribe una quantity se asiga un 1
                if servicio.quantity is None:
                    servicio.quantity = 1

                servicio.price = (tiposervicio.price * servicio.quantity)
                servicio.description = tiposervicio.name

                servicio.save()

            # Guardar en caja el monto del servicio
            caja = Caja.objects.last()
            caja.saldo = (caja.saldo + servicio.price)
            caja.save()

            response_data['result'] = "Se realizó la venta!"
            response_data['servicio_id'] = str(servicio.id)
            response_data['servicio'] = str(servicio.type_service)
            response_data['quantity'] = str(servicio.quantity)
            response_data['precio_servicio'] = str(servicio.type_service.price)
            response_data['total'] = str(servicio.price)
            response_data['vendedor'] = str(servicio.user.username)
            response_data['created_at'] = str(localize(servicio.created_at))

            # Enviar los datos a la api
            data_caja = {
                'total': str(caja.saldo),
                'date_open': str(caja.fecha_apertura),
                'date_close': str(caja.fecha_cierre)
            }
            send_to_api(data_caja, 'cashes')

            # Guardar datos de venta en la API
            data = {"name": str(servicio),
                    "price": str(servicio.type_service.price),
                    "quantity": str(servicio.quantity),
                    "seller": str(servicio.user)}
            send_to_api(data, 'services')

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            response_data['result'] = "Aun no se ha realizado la apertura de caja"
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json",
                status=500,
            )
    else:
        form = ServicioForm()
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
