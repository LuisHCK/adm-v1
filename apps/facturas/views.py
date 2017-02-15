
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Factura, FacturaItems
from .forms import FacturaForm, ItemsForm

@login_required(login_url='login') #redirect when user is not logged in

# Create your views here.
def facturas(request):
    """Ver todas las facturas"""
    facturas = Factura.objects.all()
    return render(request, 'facturas/facturas.html', {'facturas': facturas})


def nueva_factura(request):
    """Crear un nuevo factura"""
    if request.method == "POST":
        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)
            factura.usuario = request.user
            factura.save()
        messages.success(request, "La factura se creó")
        return redirect('detalles_factura', factura.pk)
    else:
        form = FacturaForm()
    return render(request, 'facturas/nueva_factura.html', {'form': form})


def cobrar_factura(request, pk):
    """Realiza el cobro de la Factura"""
    factura = get_object_or_404(Factura, pk=pk)
    items_count = FacturaItems.objects.filter(factura=factura).count()
    if items_count < 1:
        messages.error(request, "No se puede cobrar una factura sin items")
        return redirect('facturas_pagadas')
    else:
        factura.cobrar()
        messages.success(request, "Se cobró la factura")
        return redirect('detalles_factura', factura.id)


def eliminar_factura(request, pk):
    """Elimina una factura, solo si no ha sido cobrada"""
    factura = get_object_or_404(Factura, pk=pk)
    factura.delete()
    messages.success(request, "Se borró la factura")
    return redirect('facturas_pagadas')


def agregar_items(request, pk):
    """Agrega items a la factura abierta"""
    factura = get_object_or_404(Factura, pk=pk)
    if request.method == "POST":
        form = ItemsForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.factura = factura.id
            item.save()
        return redirect('detalles_factura', factura.id)
    else:
        form = ItemsForm()

    return render(request, 'facturas/detalles_factura.html', {'form': form})


def facturas_pagadas(request):
    """Muestra las facturas que ya fueron pagadas"""
    facturas = Factura.objects.filter(cobrada=True)
    return render(request, 'facturas/facturas.html', {'facturas': facturas})

def facturas_pendientes(request):
    """Muestra las facturas que ya fueron pagadas"""
    facturas = Factura.objects.filter(cobrada=False)
    return render(request, 'facturas/facturas.html', {'facturas': facturas})


def detalles_factura(request, pk):
    """Muestra los detalles de una factura"""
    factura = get_object_or_404(Factura, pk=pk)
    items = FacturaItems.objects.filter(factura=factura).all()

    if request.method == "POST":
        form = ItemsForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.factura = factura
            item.save()

            # Sumar al monto total de la factura
            factura.total = (factura.total + item.precio)
            factura.save()
            messages.success(request, "Se agregó el item")
        return redirect('detalles_factura', factura.id)
    else:
        form = ItemsForm()

    return render(request, 'facturas/detalles_factura.html', {'factura': factura, 'items': items, 'form_item': form})

def eliminar_item(request, pk):
    """Elimina un item de la factura"""
    item = get_object_or_404(FacturaItems, pk=pk)
    item.delete()

    # Resta la cantidad del total
    factura = Factura.objects.get(id=item.factura.id)
    factura.total = (factura.total + item.precio)
    factura.save()

    messages.success(request, "Se borró el item de la factura")
    return redirect('detalles_factura', item.factura.id)
