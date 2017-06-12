
import json

from django.contrib.postgres.search import SearchVector
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from apps.caja.models import Caja
from apps.common import validaciones
from apps.inventory.models import Product, Inventory
from apps.servicios.models import Service, TypeService
from apps.ventas.models import Sale
from apps.cloud.views import send_to_api

from .forms import FacturaArticuloForm, FacturaForm, ServicioRapidoForm
from .models import Invoice, InvoiceProducts, InvoiceServices


@login_required(login_url='login')  # redirect when user is not logged in
def facturas(request):
    """Ver todas las facturas"""
    lista_facturas = Invoice.objects.filter(open=False)
    lista_pendientes = Invoice.objects.filter(open=False, payment_type='credito')
    abiertas = Invoice.objects.filter(open=True).count
    lista_abiertas = Invoice.objects.filter(open=True)
    total_sin_pagar = total_facturas(lista_pendientes)
    return render(request, 'facturas/facturas.html', {
        'facturas': lista_facturas,
        'abiertas': abiertas,
        'lista_abiertas': lista_abiertas,
        'lista_pendientes': lista_pendientes,
        'total_sin_pagar': total_sin_pagar,
        'form_factura': FacturaForm,
    })


def total_facturas(facturas):
    total = 0
    for invoice in facturas:
        total += invoice.total
    return total


def facturas_pagadas(request):
    """Muestra las facturas que ya fueron pagadas"""
    lista_facturas = Invoice.objects.filter(cerrada=True)
    pendientes = Invoice.objects.filter(cerrada=False).count
    return render(request, 'facturas/facturas.html', {
        'facturas': lista_facturas,
        'pendientes': pendientes,
    })


def facturas_pendientes(request):
    """Muestra las facturas que ya fueron pagadas"""
    lista_facturas = Invoice.objects.filter(cerrada=False)
    pendientes = Invoice.objects.filter(cerrada=False).count
    return render(request, 'facturas/facturas.html', {
        'facturas': lista_facturas,
        'pendientes': pendientes,
    })


def nueva_factura(request):
    """Crear un nuevo invoice"""
    response_data = {}
    if Caja.objects.count() > 0:
        if request.method == "POST":
            form = FacturaForm(request.POST)
            if form.is_valid():
                print('form is valid :D')
                invoice = form.save(commit=False)
                invoice.user = request.user
                invoice.save()

                response_data['result'] = 'Se creó la invoice.'
                response_data['id'] = str(invoice.pk)
                response_data['client'] = str(invoice.client)
                response_data['payment_type'] = str(invoice.payment_type)

                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json")
            else:
                return HttpResponse(
                    json.dumps({'result': 'Los datos no son válidos'}),
                    content_type="application/json",
                    status=500,)

        else:
            return HttpResponse(
                json.dumps({"nothing to see": "this isn't happening"}),
                content_type="application/json",
                status=500,
            )
    else:
        response_data['result'] = 'Aún no se rea realizado la apertura de caja.'
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json",
            status=500,
        )


def cobrar_factura(request, pk):
    """Realiza el cobro de la Invoice"""
    invoice = get_object_or_404(Invoice, pk=pk)
    service_count = InvoiceProducts.objects.filter(invoice=invoice).count()
    articulos_count = InvoiceServices.objects.filter(invoice=invoice).count()
    items_count = (service_count + articulos_count)

    if Caja.objects.count() > 0:
        if items_count < 1:
            messages.error(request, "No se puede cobrar una invoice sin items")
            return redirect('facturas_pagadas')
        else:
            if request.method == "POST":
                # Obtener todos los items articulos y servicios de la invoice
                articulos = InvoiceProducts.objects.filter(invoice=invoice)
                servicios = InvoiceServices.objects.filter(invoice=invoice)

                # Realizar la venta de cada product
                for product in articulos:
                    Sale.objects.create(
                        user=request.user,
                        product=product.product,
                        quantity=product.quantity,
                        invoice=invoice,
                        total=(product.quantity * product.product.sale_price))
                    inventory = Inventory.objects.get(
                        product=product.product)
                    inventory.stocks -= product.quantity
                    inventory.save()

                # Realizar la venta de cada servicio
                for servicio in servicios:
                    Service.objects.create(
                        user=request.user,
                        description=servicio.type_service.name,
                        quantity=servicio.quantity,
                        type_service=servicio.type_service,
                        invoice=invoice,
                        price=(servicio.type_service.price * servicio.quantity))

                if invoice.payment_type == 'contado':
                    # Guardar el monto en caja
                    caja = Caja.objects.last()
                    caja.saldo += invoice.total
                    caja.save()
                    invoice.status = 'pagado'
                    invoice.save()

                    # Enviar los datos a la api
                    data = {
                        'total': str(caja.saldo),
                        'date_open': str(caja.fecha_apertura),
                        'date_close': str(caja.fecha_cierre)
                    }
                    send_to_api(data, 'cashes')

                invoice.open = False
                invoice.deadline = request.POST.get('deadline')
                invoice.save()

                # Enviar los datos a la api
                credito = None
                if invoice.payment_type == 'credito':
                    credito = True
                else:
                    credito = False

                data = {"client": str(invoice),
                        "products": articulos_count,
                        "services": service_count,
                        "total": str(invoice.total),
                        "credit": credito,
                        "code": invoice.id,
                        "seller": str(invoice.user),
                        "date_open": str(invoice.created_at),
                        "date_charged": str(invoice.pay_at)}
                send_to_api(data, 'invoices')

                return HttpResponse(
                    json.dumps({'result': 'Se cerró la invoice', 'id': str(invoice.id)}),
                    content_type="application/json")
    else:
        return HttpResponse(
            json.dumps({'result': 'No se puede cerrar la invoice'}),
            content_type="application/json",
            status=500)


def eliminar_factura(request, pk):
    """Elimina una invoice, solo si no ha sido cerrada"""
    if request.method == 'POST':
        invoice = get_object_or_404(Invoice, pk=pk)

        if validaciones.es_administrador(request.user) and invoice.cerrada is False:
            invoice.delete()
            messages.success(request, "Se borró la invoice")

            return HttpResponse(
                json.dumps({'result': 'Se eliminó la invoice'}),
                content_type="application/json")

        elif invoice.user == request.user:
            invoice.delete()
            messages.success(request, "Se borró la invoice")

            return HttpResponse(
                json.dumps({'result': 'Se eliminó la invoice'}),
                content_type="application/json")

        else:
            return HttpResponse(
                json.dumps({'result': 'No se puede eliminar la invoice'}),
                content_type="application/json",
                status=500)



def agregar_articulo(request, pk):
    """Agrega items a la invoice abierta"""
    invoice = get_object_or_404(Invoice, pk=pk)
    response_data = {}
    if request.method == "POST":
        form = FacturaArticuloForm(request.POST)
        if form.is_valid():
            item_articulos = form.save(commit=False)
            item_articulos.invoice = invoice

            inventory = get_object_or_404(
                Inventory, product=item_articulos.product)
            if item_articulos.quantity < inventory.stocks:
                item_articulos.save()

                # Suma al total de la invoice
                product = Product.objects.get(id=item_articulos.product.id)
                invoice.total += (product.sale_price *
                                  item_articulos.quantity)
                invoice.save()

                # Devolver un json con los datos del product
                response_data['result'] = 'Se agregó el product'
                response_data['item_id'] = item_articulos.pk
                response_data['product'] = str(item_articulos.product)
                response_data['articulo_id'] = str(item_articulos.product.id)
                response_data['price'] = str(
                    item_articulos.product.sale_price)
                response_data['quantity'] = str(item_articulos.quantity)
                response_data['total_factura'] = str(invoice.total)
            else:
                # Devolver una excepcion por que o hay suficientes articulos
                response_data['result'] = 'No hay suficientes articulos para vender'
                response_data['reason'] = 'Existencias disponibles: ' + \
                    str(inventory.stocks)
                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json",
                    status=410,
                )

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def eliminar_articulos(request, product):
    """Elimina un item de la invoice"""
    item = get_object_or_404(InvoiceProducts, pk=product)
    item.delete()

    # Resta la quantity del total
    invoice = Invoice.objects.get(id=item.invoice.id)
    invoice.total -= (item.product.sale_price * item.quantity)
    invoice.save()

    messages.success(request, "Se borró el item de la invoice")
    return redirect('detalles_factura', item.invoice.id)


def agregar_servicio(request, pk):
    """Agrega items a la invoice abierta"""
    response_data = {}
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == "POST":
        form = ServicioRapidoForm(request.POST)
        if form.is_valid():
            item_servicio = form.save(commit=False)
            item_servicio.invoice = invoice
            item_servicio.save()

        # Suma al total de la invoice
        servicio = TypeService.objects.get(id=item_servicio.type_service.id)
        invoice.total += (servicio.price * item_servicio.quantity)
        invoice.save()

        # Devolver un json con los datos del product
        response_data['result'] = 'Se agregó el '
        response_data['item_id'] = item_servicio.pk
        response_data['servicio'] = str(item_servicio.type_service)
        response_data['servicio_id'] = str(item_servicio.type_service.id)
        response_data['price'] = str(item_servicio.type_service.price)
        response_data['quantity'] = str(item_servicio.quantity)
        response_data['total_factura'] = str(invoice.total)

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def eliminar_servicios(request, servicio):
    """Elimina un item de la invoice"""
    item = get_object_or_404(InvoiceServices, pk=servicio)
    item.delete()

    # Resta la quantity del total
    invoice = Invoice.objects.get(id=item.invoice.id)
    invoice.total -= (item.type_service.price * item.quantity)
    invoice.save()

    messages.success(request, "Se borró el item de la invoice")
    return redirect('detalles_factura', item.invoice.id)


def detalles_factura(request, pk):
    """Muestra los detalles de una invoice"""
    invoice = get_object_or_404(Invoice, pk=pk)
    item_articulos = InvoiceProducts.objects.filter(invoice=invoice).all()
    item_servicios = InvoiceServices.objects.filter(invoice=invoice).all()
    project_ver = settings.PROJECT_VERSION

    from apps.ajustes.models import Ajuste

    return render(request, 'facturas/detalles_factura.html', {
        'invoice': invoice,
        'item_articulos': item_articulos,
        'item_servicios': item_servicios,
        'form_articulo': FacturaArticuloForm,
        'form_servicio': ServicioRapidoForm,
        'project_ver': project_ver,
        'empresa': Ajuste.objects.get(pk=1) # PENDIENTE DE LIMITAR LOS CAMPOS RETORNADOS
    })


def buscar_articulo(request, code=None):
    '''Busca los articulos en la base de datos'''
    articulos = Product.objects.annotate(
        search=SearchVector('code', 'name')).filter(search=code)

    # Serializar el objeto que contiene los resultados la busqueda
    arts = [obj.as_dict() for obj in articulos]

    return HttpResponse(
        json.dumps(arts),
        content_type="application/json",)

    # SERVICIOS


def buscar_servicio(request, code):
    '''Busca servicios por su code o name'''
    tipos_servicios = TypeService.objects.annotate(
        search=SearchVector('code', 'name')).filter(search__icontains=code)

    serv = [obj.as_dict() for obj in tipos_servicios]

    return HttpResponse(
        json.dumps(serv),
        content_type="application/json")
