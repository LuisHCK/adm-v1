
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.cash.models import Cash
from apps.inventory.models import Inventory
from apps.sales.models import Sale
from apps.cloud.views import send_to_api

from .forms import SaleForm


# Create your views here.


@login_required(login_url='login')  # redirect when user is not logged in
def Sales(request):
    """Retorna la pagina de Start"""
    sale = Sale.objects.all().order_by('-created_at')
    return render(request, 'sales/sale.html', {'sale': sale, 'form_venta': SaleForm})


def MakeSale(request):
    """Realiza la sale de un artículo"""
    # Obtener las stocks actuales del producto
    sale = object
    if request.method == "POST":
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            # Registra el user que realiza la sale
            sale.user = request.user
            # Calcula el total de la sale
            sale.total = (sale.product.sale_price * sale.quantity)
            sale.save()

        # Restar producto del inventory
        inventory = Inventory.objects.get(product=sale.product)

        # Si la quantity es nula o menor a uno se le asigna un 1
        if sale.quantity < 1:
            sale.quantity = 1

        inventory.stocks = (inventory.stocks - sale.quantity)
        inventory.save()

        # Guardar en Cash
        cash = Cash.objects.last()
        if cash:
            cash.balance = (cash.balance + sale.total)
            cash.save()
        else:
            Cash.objects.create(balance=sale.total, user=request.user)

        # Enviar los datos a la api
        data_caja = {
            'total': str(cash.balance),
            'date_open': str(cash.opening_date),
            'date_close': str(cash.closing_date)
        }
        send_to_api(data_caja, 'cashes')

        # Guardar datos de sale en la API
        data = {"product": str(sale.product),
                "price": str(sale.product.sale_price),
                "quantity": str(sale.quantity),
                "seller": str(sale.user)}
        send_to_api(data, 'sales')

        return redirect('sales')

    else:
        form = SaleForm()
    return render(request, 'sales/nueva.html', {'form': form})
