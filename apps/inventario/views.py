
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
import json
from apps.inventario.models import Inventario, Articulos
from .forms import ArticuloForm, InventarioForm

# Create your views here.


@login_required(login_url='login')  # redirect when user is not logged in
def lista_inventario(request):
    """"Retorna la lista de los articulos en el inventario"""
    inventario = Inventario.objects.select_related().all().order_by('-id')
    # calcular el total de dinero invertido en el Inventario
    total_inversion = 0
    for inv in inventario:
        total_inversion += (inv.articulo.precio_venta * inv.existencias)
    return render(request, 'inventario/lista_inventario.html', {
        'inventario': inventario,
        'total_inversion': total_inversion,
        'form_articulo': ArticuloForm,
    })


def detalles_articulo(request, pk):
    """Ver detalles de un articulo"""
    articulo = get_object_or_404(Articulos, pk=pk)
    existencias = Inventario.objects.only('existencias').get(articulo=articulo)
    return render(request, 'inventario/detalles_articulo.html',
                  {
                      'articulo': articulo,
                      'existencias': existencias,
                      'form': InventarioForm
                  })


def nuevo_articulo(request):
    """Crear un nuevo articulo"""
    if request.method == "POST":
        form = ArticuloForm(request.POST)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.save()
        # Agregar el producto al inventario
        Inventario.objects.create(articulo=articulo, existencias=0)
        return redirect('ver_articulo', articulo.id)
    else:
        form = ArticuloForm()
    return render(request, 'inventario/editar_articulo.html', {'form': form})


def nuevo_articulo_ajax(request):
    """Crear un nuevo articulo"""
    response_data = {}
    if request.method == "POST":
        form = ArticuloForm(request.POST)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.save()
        # Agregar el producto al inventario
        Inventario.objects.create(articulo=articulo, existencias=0)

        response_data['result'] = "Se creó correctamente el artículo"
        response_data['articulo_id'] = str(articulo.id)
        response_data['nombre'] = str(articulo)
        response_data['precio_venta'] = str(articulo.precio_venta)
        response_data['precio_compra'] = str(articulo.precio_compra)

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
    """Edita las existencias de un articulo en el inventario"""
    inventario = get_object_or_404(Inventario, pk=pk)
    response_data = {}
    if request.method == "POST":
        inventario.existencias = request.POST['existencias']
        inventario.minimo_existencias = request.POST['minimo_existencias']
        inventario.save()

        response_data['result'] = str('El inventario se actualizó con éxito')
        response_data['existencias'] = str(inventario.existencias)
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
    """Elimina un articulo"""
    response_data = {}

    if request.method == "POST":
        articulo = Articulos.objects.get(pk=pk)
        response_data['articulo_id'] = str(articulo.id)
        articulo.delete()
        response_data['result'] = "Se eliminó con exito"
        response_data['articulo'] = str(articulo)
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
