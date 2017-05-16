
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.utils.formats import localize

import json
from apps.caja.models import Caja
from apps.facturas.models import Factura, FacturaItems
from .models import Servicio, TipoServicio
from .forms import ServicioForm, TipoServicioForm


@login_required(login_url='login')  # redirect when user is not logged in
# Create your views here.
def inicio(request):
    """Devuelve los servicios realizados"""
    servicios = Servicio.objects.all().order_by('-fecha_servicio')
    facturas = Factura.objects.filter(estado='cerrado')
    tipos_sericios = TipoServicio.objects.all()
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
                servicio.usuario = request.user

                # Asignar el precio del servicio segun el tipo de servicio
                tiposervicio = TipoServicio.objects.get(
                    id=servicio.tipo_servicio.id)
                servicio.tipo_servicio = tiposervicio

                # Calcular el precio en base a la cantidad de producto

                # Si no se escribe una cantidad se asiga un 1
                if servicio.cantidad is None:
                    servicio.cantidad = 1

                servicio.precio = (tiposervicio.costo * servicio.cantidad)
                servicio.descripcion = tiposervicio.nombre

                servicio.save()

            # Guardar en caja el monto del servicio
            caja.saldo = (caja.saldo + servicio.precio)
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

    if request.method == "POST":
        form = TipoServicioForm(request.POST)
        if form.is_valid():
            tipo_servicio = form.save(commit=False)
            tipo_servicio.save()

            response_data['result'] = "Se guardó el nuevo tipo de Servicio"
            response_data['id'] = str(tipo_servicio.id)
            response_data['nombre'] = str(tipo_servicio.nombre)
            response_data['costo'] = str(tipo_servicio.costo)
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        form = TipoServicioForm()
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def agregar_a_factura(request, pk, fact):
    """Agrega un servicio como item de factura"""
    servicio = get_object_or_404(Servicio, id=pk)
    factura = get_object_or_404(Factura, id=fact)
    FacturaItems.objects.create(
        factura=factura,
        concepto=servicio.descripcion,
        precio=servicio.precio
        )
    factura.total += servicio.precio
    factura.save()
    return redirect('servicios_realizados')


def servicio_activacion(request, pk):
    tiposervicio = get_object_or_404(TipoServicio, pk=pk)
    response_data = {}
    if request.method == "POST" and request.is_ajax():
        tiposervicio.activo = True
        tiposervicio.save()
        response_data['result'] = "Se Activó el Servicio: " + tiposervicio.nombre
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    elif request.method == "UPDATE" and request.is_ajax():
        tiposervicio.activo = False
        tiposervicio.save()
        response_data['result'] = "Se desactivó el Servicio: " + tiposervicio.nombre
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
