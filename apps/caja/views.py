
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import CajaForm, EgresoForm
from .models import Caja, Capital, Egresos
from apps.common import validaciones

@login_required(login_url='login') #redirect when user is not logged in

def inicio(request):
    """Muestra el estado actual de la caja"""
    caja = Caja.objects.all().order_by('-fecha_apertura')
    return render(request, 'caja/caja.html', {'caja': caja})


def apertura_caja(request):
    """Abre el uso de la caja"""
    caja = Caja.objects.last()
    if caja:
        return redirect('caja_inicio')
    else:
        if request.method == 'POST' and validaciones.es_administrador(request.user):
            form = CajaForm(request.POST)
            if form.is_valid():
                caja = form.save(commit=False)
                caja.usuario = request.user
                caja.save()
            messages.success(request, "Se realizó la apertura.")
            return redirect('caja_inicio')
        else:
            form = CajaForm()
        return render(request, 'caja/saldo_form.html', {'form': form})


def cierre_caja(request, saldo):
    """Cierra caja y se retira el dinero"""
    ultima_caja = Caja.objects.last()
    if request.method == "POST":
        if validaciones.es_administrador(request.user):
            form = CajaForm(request.POST)
            # Actualizar el saldo en caja
            ultima_caja.saldo = saldo
            ultima_caja.fecha_cierre = str(timezone.now())
            ultima_caja.save()

                # Guardar el monto extrído en el Capital
            capital = Capital.objects.last()
            if capital:
                capital.monto = (capital.monto + caja.saldo)
                capital.save()
            else:
                Capital.objects.create(monto=caja.saldo)
            messages.success(request, "Se realizó el cierre")
            return redirect('caja_inicio')
        else:
            messages.success(request, "No tienes permisos para esta acción")
            return redirect('caja_inicio')

    else:
        form = CajaForm()
    return render(request, 'caja/saldo_form.html', {'form': form, 'ultima_caja': ultima_caja})


def egreso_caja(request):
    """Realiza un retiro de dinero de la caja abierta"""
    if request.method == "POST":
        form = EgresoForm(request.POST)
        if form.is_valid():
            egreso = form.save(commit=False)
            egreso.usuario = request.user
            egreso.save()

        # Restar del saldo de caja la cantidad del egreso
        caja = Caja.objects.last()
        caja.saldo = (caja.saldo - egreso.cantidad)
        caja.save()

        return redirect('detalles_egreso', egreso.id)
    else:
        form = EgresoForm()
    return render(request, 'egresos/egreso_form.html', {'form': form})


def ver_egresos(request):
    """Muestra todos los egresos realizados"""
    egresos = Egresos.objects.all()
    return render(request, 'egresos/egresos.html', {'egresos': egresos})


def detalles_egreso(request, pk):
    """Ver detalles de un egreso"""
    egreso = get_object_or_404(Egresos, pk=pk)
    return render(request, 'egresos/detalles_egreso.html', {'egreso': egreso})


def estado_capital(request):
    """Mostar el capital con el que se cuenta"""
    capital = Capital.objects.first()
    return render(request, 'capital/capital.html', {'capital': capital})
