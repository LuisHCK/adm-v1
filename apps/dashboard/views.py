
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
