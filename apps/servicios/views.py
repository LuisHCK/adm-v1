
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.caja.models import Caja
from apps.facturas.models import Factura, FacturaItems
from .models import Servicio, TipoServicio
from .forms import ServicioForm


@login_required(login_url='login')  # redirect when user is not logged in
# Create your views here.
def inicio(request):
    """Devuelve los servicios realizados"""
    servicios = Servicio.objects.all().order_by('-fecha_servicio')
    facturas = Factura.objects.filter(cobrada=False)
    return render(request, 'servicios/servicios.html',
                  {'servicios': servicios, 'facturas': facturas})


def realizar_servicio(request):
    """Realiza un registro del servicio realizado"""
    caja = Caja.objects.last()
    if request.method == "POST":
        form = ServicioForm(request.POST)
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
        caja.saldo = (caja.saldo + servicio.precio)
        caja.save()

        messages.success(request, "Se realizó el servicio")
        return redirect('servicios_realizados')
    else:
        form = ServicioForm()
    return render(request, 'servicios/servicio_form.html', {'form': form})


def agregar_a_factura(request, pk, fact):
    """Agrega un servicio como item de factura"""
    servicio = get_object_or_404(Servicio, id=pk)
    factura = get_object_or_404(Factura, id=fact)
    FacturaItems.objects.create(
        factura=factura,
        concepto=servicio.descripcion,
        precio=servicio.precio
        )
    factura.total += servicio.precio
    factura.save()
    return redirect('servicios_realizados')
