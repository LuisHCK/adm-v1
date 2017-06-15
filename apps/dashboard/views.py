
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.formats import localize

from apps.cash.models import Cash
from apps.cloud.views import send_to_api
from apps.inventory.models import Inventory
from apps.services.forms import ServiceForm, TypeService
from apps.services.models import Service
from apps.sales.models import Sale

from .forms import SaleForm


@login_required(login_url='login') #redirect when user is not logged in

# Create your views here.
def Start(request):
    """Retorna la pagina de Start"""
    sale = Sale.objects.all().order_by('-created_at')[:5]
    services = Service.objects.all().order_by('-created_at')[:5]
    cash = Cash.objects.last()
    count_services = Service.objects.count()
    # Realiza la sale de un artículo
    if request.method == "POST":
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)

            # Registra el user que realiza la sale
            sale.user = request.user

            # Calcula el total de la sale
            sale.total = sale.product.sale_price * sale.quantity

            # Guardar la sale realizada
            sale.save()

            # Restar producto del inventory
            inventory = Inventory.objects.get(product=sale.product)
            inventory.stocks = (inventory.stocks - sale.quantity)
            inventory.save()

            # Guardar en Cash
            cash = Cash.objects.last()
            if cash:
                cash.balance += sale.total
                cash.save()
            else:
                Cash.objects.create(balance=sale.total, user=request.user)

        return redirect('Start')
    else:
        form = SaleForm()
        form2 = ServiceForm()
    return render(request, 'dashboard/dashboard.html',
                  {'sale': sale, 'cash': cash, 'count_services': count_services,
                   'services': services, 'form_venta': form, 'form_service': form2})

def ServiceAjax(request):
    """Realiza un registro del service realizado"""
    response_data = {}

    if request.method == "POST":
        form = ServiceForm(request.POST)

        if Cash.objects.count() > 0:
            if form.is_valid():
                service = form.save(commit=False)
                service.user = request.user

                # Asignar el price del service segun el tipo de service
                service_type = TypeService.objects.get(
                    id=service.type_service.id)
                service.type_service = service_type

                # Calcular el price en base a la quantity de producto

                # Si no se escribe una quantity se asiga un 1
                if service.quantity is None:
                    service.quantity = 1

                service.price = (service_type.price * service.quantity)
                service.description = service_type.name

                service.save()

            # Guardar en cash el monto del service
            cash = Cash.objects.last()
            cash.balance = (cash.balance + service.price)
            cash.save()

            response_data['result'] = "Se realizó la sale!"
            response_data['servicio_id'] = str(service.id)
            response_data['service'] = str(service.type_service)
            response_data['quantity'] = str(service.quantity)
            response_data['precio_servicio'] = str(service.type_service.price)
            response_data['total'] = str(service.price)
            response_data['seller'] = str(service.user.username)
            response_data['created_at'] = str(localize(service.created_at))

            # Enviar los datos a la api
            data_caja = {
                'total': str(cash.balance),
                'date_open': str(cash.opening_date),
                'date_close': str(cash.closing_date)
            }
            send_to_api(data_caja, 'cashes')

            # Guardar datos de sale en la API
            data = {"name": str(service),
                    "price": str(service.type_service.price),
                    "quantity": str(service.quantity),
                    "seller": str(service.user)}
            send_to_api(data, 'services')

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            response_data['result'] = "Aun no se ha realizado la apertura de cash"
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json",
                status=500,
            )
    else:
        form = ServiceForm()
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
