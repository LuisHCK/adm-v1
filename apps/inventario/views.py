
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
import json
from apps.inventario.models import Inventory, Product
from .forms import ArticuloForm, InventarioForm

# Create your views here.


@login_required(login_url='login')  # redirect when user is not logged in
def lista_inventario(request):
    """"Retorna la lista de los articulos en el inventario"""
    inventario = Inventory.objects.select_related().all().order_by('-id').filter(active=True)
    # calcular el total de dinero invertido en el Inventory
    total_inversion = 0
    for inv in inventario:
        total_inversion += (inv.product.sale_price * inv.stocks)
    return render(request, 'inventario/lista_inventario.html', {
        'inventario': inventario,
        'total_inversion': total_inversion,
        'form_articulo': ArticuloForm,
    })


def detalles_articulo(request, pk):
    """Ver detalles de un product"""
    product = get_object_or_404(Product, pk=pk)
    stocks = Inventory.objects.only('stocks').get(product=product)
    form_art = ArticuloForm()
    return render(request, 'inventario/detalles_articulo.html',
                  {
                      'product': product,
                      'stocks': stocks,
                      'form': InventarioForm
                  })


def nuevo_articulo(request):
    """Crear un nuevo product"""
    if request.method == "POST":
        form = ArticuloForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
        # Agregar el producto al inventario
        Inventory.objects.create(product=product, stocks=0)
        return redirect('ver_articulo', product.id)
    else:
        form = ArticuloForm()
    return render(request, 'inventario/editar_articulo.html', {'form': form})


def nuevo_articulo_ajax(request):
    """Crear un nuevo product"""
    response_data = {}
    if request.method == "POST":
        form = ArticuloForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
        # Agregar el producto al inventario
        Inventory.objects.create(product=product, stocks=product.initial_ammount)
        # Obtener el artículo del inventario y asignarle un mínimo por defecto
        inventario = Inventory.objects.get(product=product)
        inventario.min_stocks = 1
        inventario.save()

        response_data['result'] = "Se creó correctamente el artículo"
        response_data['articulo_id'] = str(product.id)
        response_data['name'] = str(product)
        response_data['code'] = str(product.code)
        response_data['sale_price'] = str(product.sale_price)
        response_data['purchase_price'] = str(product.purchase_price)
        response_data['sale_price2'] = str(product.sale_price2)
        response_data['sale_price3'] = str(product.sale_price3)
        response_data['iva'] = str(product.iva)
        response_data['initial_ammount'] = str(product.initial_ammount)
        response_data['min_stocks'] = str(inventario.min_stocks)

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def actualizar_existencias(request, pk):
    """Edita las stocks de un product en el inventario"""
    inventario = get_object_or_404(Inventory, pk=pk)
    response_data = {}
    if request.method == "POST":
        inventario.stocks = request.POST['stocks']
        inventario.min_stocks = request.POST['min_stocks']
        inventario.active = request.POST['active']
        inventario.save()

        response_data['result'] = str('El inventario se actualizó con éxito')
        response_data['stocks'] = str(inventario.stocks)
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def eliminar_articulo_ajax(request, pk):
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
