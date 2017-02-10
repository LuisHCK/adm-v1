
from django.shortcuts import render, get_object_or_404, redirect
from apps.inventario.models import Inventario, Articulos
from .forms import ArticuloForm, InventarioForm
from apps.ventas.models import Venta

# Create your views here.


def lista_inventario(request):
    """"Retorna la lista de los articulos en el inventario"""
    inventario = Inventario.objects.select_related().all()
    return render(request, 'inventario/lista_inventario.html', {'inventario': inventario})


def detalles_articulo(request, pk):
    """Ver detalles de un articulo"""
    articulo = get_object_or_404(Articulos, pk=pk)
    return render(request, 'inventario/detalles_articulo.html', {'articulo': articulo})


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


def actualizar_existencias(request, pk):
    """Edita las existencias de un articulo en el inventario"""
    inventario = get_object_or_404(Inventario, pk=pk)
    if request.method == "POST":
        form = InventarioForm(request.POST, instance=inventario)
        if form.is_valid():
            inventario = form.save(commit=False)
            inventario.save()
        return redirect('ver_inventario')
    else:
        form = InventarioForm(instance=inventario)
    return render(request, 'inventario/editar_existencias.html', {'form': form})
