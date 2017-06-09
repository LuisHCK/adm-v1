
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.utils.formats import localize

import json
from apps.caja.models import Caja
from apps.facturas.models import Invoice, InvoiceItems
from .models import Service, TypeService
from .forms import ServicioForm, TipoServicioForm


@login_required(login_url='login')  # redirect when user is not logged in
# Create your views here.
def inicio(request):
    """Devuelve los servicios realizados"""
    servicios = Service.objects.all().order_by('-created_at')
    facturas = Invoice.objects.filter(status='cerrado')
    tipos_sericios = TypeService.objects.all()
    return render(request, 'servicios/servicios.html',
                  {
                      'servicios': servicios,
                      'facturas': facturas,
                      'form_servicio': ServicioForm,
                      'form_tipo_sericio': TipoServicioForm,
                      'tipos_servicio': tipos_sericios,
                      })


def realizar_servicio(request):
    """Realiza un registro del servicio realizado"""
    caja = Caja.objects.last()
    if request.method == "POST":
        form = ServicioForm(request.POST)

        if hasattr(caja, 'saldo'):
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
            caja.saldo = (caja.saldo + servicio.price)
            caja.save()

            messages.success(request, "Se realizó el servicio")
            return redirect('servicios_realizados')
        else:
            messages.error(request, "Aún no se ha realizado la apertura de caja.")
            return redirect('servicios_realizados')

    else:
        form = ServicioForm()
    return render(request, 'servicios/servicio_form.html', {'form': form})


def tipo_servicio_ajax(request):
    """Realiza un registro del servicio realizado"""
    response_data = {}
    from apps.common.validaciones import es_administrador
    if request.method == "POST" and es_administrador(request.user):
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
                json.dumps({"result": "Ocurrió un error al guardar el tipo de servicio"}),
                content_type="application/json",
                status=500)
    else:
        return HttpResponse(
            json.dumps({"result": "No estas autorizado para esta acción"}),
            content_type="application/json",
            status=500)

def agregar_a_factura(request, pk, fact):
    """Agrega un servicio como item de invoice"""
    servicio = get_object_or_404(Service, id=pk)
    invoice = get_object_or_404(Invoice, id=fact)
    InvoiceItems.objects.create(
        invoice=invoice,
        details=servicio.description,
        price=servicio.price
        )
    invoice.total += servicio.price
    invoice.save()
    return redirect('servicios_realizados')


def servicio_activacion(request, pk):
    tiposervicio = get_object_or_404(TypeService, pk=pk)
    response_data = {}
    if request.method == "POST" and request.is_ajax():
        tiposervicio.active = True
        tiposervicio.save()
        response_data['result'] = "Se Activó el Service: " + tiposervicio.name
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    elif request.method == "UPDATE" and request.is_ajax():
        tiposervicio.active = False
        tiposervicio.save()
        response_data['result'] = "Se desactivó el Service: " + tiposervicio.name
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
