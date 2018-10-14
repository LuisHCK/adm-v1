
import json

from django.contrib.postgres.search import SearchVector
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from apps.cash.models import Cash
from apps.common import validaciones
from apps.inventory.models import Product, Inventory
from apps.services.models import Service, TypeService
from apps.sales.models import Sale
from apps.cloud.views import send_to_api

from .forms import InvoiceProductForm, InvoiceForm, FastServiceForm
from .models import Invoice, InvoiceProducts, InvoiceServices


@login_required(login_url='login')  # redirect when user is not logged in
def AllInvoices(request):
    """Ver todas las invoices"""
    list_invoices = Invoice.objects.filter(open=False)
    list_pending = Invoice.objects.filter(open=False, payment_type='credit')
    opened = Invoice.objects.filter(open=True).count
    list_opened = Invoice.objects.filter(open=True)
    total_pending = TotalInvoices(list_pending)
    return render(request, 'invoices/invoices.html', {
        'invoices': list_invoices,
        'opened': opened,
        'list_opened': list_opened,
        'list_pending': list_pending,
        'total_pending': total_pending,
        'invoice_form': InvoiceForm,
    })


def TotalInvoices(invoices):
    total = 0
    for invoice in invoices:
        total += invoice.total
    return total


def InvoicesPaid(request):
    """Muestra las invoices que ya fueron pagadas"""
    list_invoices = Invoice.objects.filter(closed=True)
    pending = Invoice.objects.filter(closed=False).count
    return render(request, 'invoices/invoices.html', {
        'invoices': list_invoices,
        'pending': pending,
    })


def PendingInvoices(request):
    """Muestra las invoices que ya fueron pagadas"""
    list_invoices = Invoice.objects.filter(closed=False)
    pending = Invoice.objects.filter(closed=False).count
    return render(request, 'invoices/invoices.html', {
        'invoices': list_invoices,
        'pending': pending,
    })


def NewInvoice(request):
    """Crear un nuevo invoice"""
    response_data = {}
    if Cash.objects.count() > 0:
        if request.method == "POST":
            form = InvoiceForm(request.POST)
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
        response_data['result'] = 'Aún no se rea realizado la apertura de cash.'
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json",
            status=500,
        )


def BillInvoice(request, pk):
    """Realiza el cobro de la Invoice"""
    invoice = get_object_or_404(Invoice, pk=pk)
    service_count = InvoiceProducts.objects.filter(invoice=invoice).count()
    products_count = InvoiceServices.objects.filter(invoice=invoice).count()
    items_count = (service_count + products_count)

    if Cash.objects.count() > 0:
        if items_count < 1:
            messages.error(request, "No se puede cobrar una invoice sin items")
            return redirect('InvoicesPaid')
        else:
            if request.method == "POST":
                # Obtener todos los items products y services de la invoice
                products = InvoiceProducts.objects.filter(invoice=invoice)
                services = InvoiceServices.objects.filter(invoice=invoice)

                # Realizar la sale de cada product
                for product in products:
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

                # Realizar la sale de cada service
                for service in services:
                    Service.objects.create(
                        user=request.user,
                        description=service.type_service.name,
                        quantity=service.quantity,
                        type_service=service.type_service,
                        invoice=invoice,
                        price=(service.type_service.price * service.quantity))

                if invoice.payment_type == 'contado':
                    # Guardar el monto en cash
                    cash = Cash.objects.last()
                    cash.balance += invoice.total
                    cash.save()
                    invoice.status = 'pagado'
                    invoice.save()

                    # Enviar los datos a la api
                    data = {
                        'total': str(cash.balance),
                        'date_open': str(cash.opening_date),
                        'date_close': str(cash.closing_date)
                    }
                    send_to_api(data, 'cashes')

                invoice.open = False
                invoice.deadline = request.POST.get('deadline')
                invoice.save()

                # Enviar los datos a la api
                credit = None
                if invoice.payment_type == 'credit':
                    credit = True
                else:
                    credit = False

                data = {"client": str(invoice),
                        "products": products_count,
                        "services": service_count,
                        "total": str(invoice.total),
                        "credit": credit,
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


def DeleteInvoice(request, pk):
    """Elimina una invoice, solo si no ha sido closed"""
    if request.method == 'POST':
        invoice = get_object_or_404(Invoice, pk=pk)

        if validaciones.is_admin(request.user) and invoice.closed is False:
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



def AddProduct(request, pk):
    """Agrega items a la invoice abierta"""
    invoice = get_object_or_404(Invoice, pk=pk)
    response_data = {}
    if request.method == "POST":
        form = InvoiceProductForm(request.POST)
        if form.is_valid():
            product_items = form.save(commit=False)
            product_items.invoice = invoice

            inventory = get_object_or_404(
                Inventory, product=product_items.product)
            if product_items.quantity < inventory.stocks:
                product_items.save()

                # Suma al total de la invoice
                product = Product.objects.get(id=product_items.product.id)
                invoice.total += (product.sale_price *
                                  product_items.quantity)
                invoice.save()

                # Devolver un json con los datos del product
                response_data['result'] = 'Se agregó el product'
                response_data['item_id'] = product_items.pk
                response_data['product'] = str(product_items.product)
                response_data['product_id'] = str(product_items.product.id)
                response_data['price'] = str(
                    product_items.product.sale_price)
                response_data['quantity'] = str(product_items.quantity)
                response_data['total_invoice'] = str(invoice.total)
            else:
                # Devolver una excepcion por que o hay suficientes products
                response_data['result'] = 'No hay suficientes products para vender'
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


def DeleteProduct(request, product):
    """Elimina un item de la invoice"""
    item = get_object_or_404(InvoiceProducts, pk=product)
    item.delete()

    # Resta la quantity del total
    invoice = Invoice.objects.get(id=item.invoice.id)
    invoice.total -= (item.product.sale_price * item.quantity)
    invoice.save()

    messages.success(request, "Se borró el item de la invoice")
    return redirect('InvoiceDetails', item.invoice.id)


def AddService(request, pk):
    """Agrega items a la invoice abierta"""
    response_data = {}
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == "POST":
        form = FastServiceForm(request.POST)
        if form.is_valid():
            service_item = form.save(commit=False)
            service_item.invoice = invoice
            service_item.save()

        # Suma al total de la invoice
        service = TypeService.objects.get(id=service_item.type_service.id)
        invoice.total += (service.price * service_item.quantity)
        invoice.save()

        # Devolver un json con los datos del product
        response_data['result'] = 'Se agregó el '
        response_data['item_id'] = service_item.pk
        response_data['service'] = str(service_item.type_service)
        response_data['service_id'] = str(service_item.type_service.id)
        response_data['price'] = str(service_item.type_service.price)
        response_data['quantity'] = str(service_item.quantity)
        response_data['total_invoice'] = str(invoice.total)

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def DeleteService(request, service):
    """Elimina un item de la invoice"""
    item = get_object_or_404(InvoiceServices, pk=service)
    item.delete()

    # Resta la quantity del total
    invoice = Invoice.objects.get(id=item.invoice.id)
    invoice.total -= (item.type_service.price * item.quantity)
    invoice.save()

    messages.success(request, "Se borró el item de la invoice")
    return redirect('InvoiceDetails', item.invoice.id)


def InvoiceDetails(request, pk):
    """Muestra los detalles de una invoice"""
    invoice = get_object_or_404(Invoice, pk=pk)
    product_items = InvoiceProducts.objects.filter(invoice=invoice).all()
    service_items = InvoiceServices.objects.filter(invoice=invoice).all()
    project_ver = settings.PROJECT_VERSION

    from apps.settings.models import Settings

    return render(request, 'invoices/invoice_details.html', {
        'invoice': invoice,
        'product_items': product_items,
        'service_items': service_items,
        'form_product': InvoiceProductForm,
        'form_service': FastServiceForm,
        'project_ver': project_ver,
        'business': Settings.objects.get(pk=1) # PENDIENTE DE LIMITAR LOS CAMPOS RETORNADOS
    })


def SearchProduct(request, code=None):
    '''Busca los products en la base de datos'''
    products = Product.objects.annotate(
        search=SearchVector('code', 'name')).filter(search=code)

    # Serializar el objeto que contiene los resultados la busqueda
    arts = [obj.as_dict() for obj in products]

    return HttpResponse(
        json.dumps(arts),
        content_type="application/json",)

    # SERVICIOS


def SearchService(request, code):
    '''Busca services por su code o name'''
    type_service = TypeService.objects.annotate(
        search=SearchVector('code', 'name')).filter(search__icontains=code)

    serv = [obj.as_dict() for obj in type_service]

    return HttpResponse(
        json.dumps(serv),
        content_type="application/json")
