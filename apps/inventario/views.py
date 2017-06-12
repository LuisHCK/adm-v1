
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
import json
from apps.inventory.models import Inventory, Product
from .forms import ProductForm, InventoryForm

# Create your views here.


@login_required(login_url='login')  # redirect when user is not logged in
def InventoryList(request):
    """"Retorna la lista de los articulos en el inventory"""
    inventory = Inventory.objects.select_related(
    ).all().order_by('-id').filter(active=True)
    # calcular el total de dinero invertido en el Inventory
    total_inversion = 0
    for inv in inventory:
        total_inversion += (inv.product.sale_price * inv.stocks)
    return render(request, 'inventory/InventoryList.html', {
        'inventory': inventory,
        'total_inversion': total_inversion,
        'form_articulo': ProductForm,
    })


def ProductDetails(request, pk):
    """Ver detalles de un product"""
    product = get_object_or_404(Product, pk=pk)
    stocks = Inventory.objects.only('stocks').get(product=product)
    form_art = ProductForm()
    return render(request, 'inventory/ProductDetails.html',
                  {
                      'product': product,
                      'stocks': stocks,
                      'form': InventoryForm
                  })


def NewProduct(request):
    """Crear un nuevo product"""
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
        # Agregar el producto al inventory
        Inventory.objects.create(product=product, stocks=0)
        return redirect('ver_articulo', product.id)
    else:
        form = ProductForm()
    return render(request, 'inventory/editar_articulo.html', {'form': form})


def NewProductAjax(request):
    """Crear un nuevo product"""
    response_data = {}
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
        # Agregar el producto al inventory
        Inventory.objects.create(
            product=product, stocks=product.initial_ammount)
        # Obtener el artículo del inventory y asignarle un mínimo por defecto
        inventory = Inventory.objects.get(product=product)
        inventory.min_stocks = 1
        inventory.save()

        response_data = {
            'result': "Se creó correctamente el artículo",
            'articulo_id': str(product.id),
            'name': str(product),
            'code': str(product.code),
            'sale_price': str(product.sale_price),
            'purchase_price': str(product.purchase_price),
            'sale_price2': str(product.sale_price2),
            'sale_price3': str(product.sale_price3),
            'iva': str(product.iva),
            'initial_ammount': str(product.initial_ammount),
            'min_stocks': str(inventory.min_stocks),
        }

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def UpdateStock(request, pk):
    """Edita las stocks de un product en el inventory"""
    inventory = get_object_or_404(Inventory, pk=pk)
    response_data = {}
    if request.method == "POST":
        inventory.stocks = request.POST['stocks']
        inventory.min_stocks = request.POST['min_stocks']
        inventory.active = request.POST['active']
        inventory.save()

        response_data['result'] = str('El inventory se actualizó con éxito')
        response_data['stocks'] = str(inventory.stocks)
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def DeleteProductAjax(request, pk):
    """Elimina un product"""
    response_data = {}

    if request.method == "POST":
        product = Product.objects.get(pk=pk)
        response_data['articulo_id'] = str(product.id)
        product.delete()
        response_data['result'] = "Se eliminó con exito"
        response_data['product'] = str(product)
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
