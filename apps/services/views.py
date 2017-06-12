
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.utils.formats import localize

import json
from apps.cash.models import Cash
from apps.invoices.models import Invoice, InvoiceItems
from .models import Service, TypeService
from .forms import ServiceForm, TipoServicioForm


@login_required(login_url='login')  # redirect when user is not logged in
# Create your views here.
def Start(request):
    """Devuelve los services realizados"""
    services = Service.objects.all().order_by('-created_at')
    invoices = Invoice.objects.filter(status='cerrado')
    tipos_sericios = TypeService.objects.all()
    return render(request, 'services/services.html',
                  {
                      'services': services,
                      'invoices': invoices,
                      'form_service': ServiceForm,
                      'form_tipo_sericio': TipoServicioForm,
                      'tipos_servicio': tipos_sericios,
                      })


def PerformService(request):
    """Realiza un registro del service realizado"""
    cash = Cash.objects.last()
    if request.method == "POST":
        form = ServiceForm(request.POST)

        if hasattr(cash, 'balance'):
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
            cash.balance = (cash.balance + service.price)
            cash.save()

            messages.success(request, "Se realizó el service")
            return redirect('servicios_realizados')
        else:
            messages.error(request, "Aún no se ha realizado la apertura de cash.")
            return redirect('servicios_realizados')

    else:
        form = ServiceForm()
    return render(request, 'services/servicio_form.html', {'form': form})


def TypeServiceAjax(request):
    """Realiza un registro del service realizado"""
    response_data = {}
    from apps.common.validaciones import is_admin
    if request.method == "POST" and is_admin(request.user):
        form = TipoServicioForm(request.POST)
        if form.is_valid():
            type_service = form.save(commit=False)
            type_service.save()

            response_data['result'] = "Se guardó el nuevo tipo de Service"
            response_data['id'] = str(type_service.id)
            response_data['name'] = str(type_service.name)
            response_data['price'] = str(type_service.price)
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json")
        else:
            return HttpResponse(
                json.dumps({"result": "Ocurrió un error al guardar el tipo de service"}),
                content_type="application/json",
                status=500)
    else:
        return HttpResponse(
            json.dumps({"result": "No estas autorizado para esta acción"}),
            content_type="application/json",
            status=500)

def AddToInvoice(request, pk, fact):
    """Agrega un service como item de invoice"""
    service = get_object_or_404(Service, id=pk)
    invoice = get_object_or_404(Invoice, id=fact)
    InvoiceItems.objects.create(
        invoice=invoice,
        details=service.description,
        price=service.price
        )
    invoice.total += service.price
    invoice.save()
    return redirect('servicios_realizados')


def ActivateService(request, pk):
    service_type = get_object_or_404(TypeService, pk=pk)
    response_data = {}
    if request.method == "POST" and request.is_ajax():
        service_type.active = True
        service_type.save()
        response_data['result'] = "Se Activó el Service: " + service_type.name
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    elif request.method == "UPDATE" and request.is_ajax():
        service_type.active = False
        service_type.save()
        response_data['result'] = "Se desactivó el Service: " + service_type.name
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    else:
        response_data['result'] = "Ocurrió un error al realizar la acción"
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json",
            status=410,
        )
