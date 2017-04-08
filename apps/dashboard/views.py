
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.formats import localize
import json
from apps.ventas.models import Venta
from apps.inventario.models import Inventario
from apps.caja.models import Caja
from apps.servicios.models import Servicio
from apps.servicios.forms import ServicioForm, TipoServicio
from .forms import VentaForm

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

def venta_ajax(request):
    """Realiza la venta de un artículo"""
    # Obtener las existencias actuales del producto
    response_data = {}
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

        response_data['result'] = "Se realizó la venta!"
        response_data['venta_id'] = str(venta.id)
        response_data['articulo'] = str(venta.articulo)
        response_data['cantidad'] = str(venta.cantidad)
        response_data['precio_venta'] = str(venta.articulo.precio_venta)
        response_data['precio_compra'] = str(venta.articulo.precio_compra)
        response_data['total'] = str(venta.total)
        response_data['vendedor'] = str(venta.usuario.username)
        response_data['fecha_venta'] = str(localize(venta.fecha_venta))

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
            caja = Caja.objects.last()
            caja.saldo = (caja.saldo + servicio.precio)
            caja.save()

            response_data['result'] = "Se realizó la venta!"
            response_data['servicio_id'] = str(servicio.id)
            response_data['servicio'] = str(servicio.tipo_servicio)
            response_data['cantidad'] = str(servicio.cantidad)
            response_data['precio_servicio'] = str(servicio.tipo_servicio.costo)
            response_data['total'] = str(servicio.precio)
            response_data['vendedor'] = str(servicio.usuario.username)
            response_data['fecha_servicio'] = str(localize(servicio.fecha_servicio))
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

