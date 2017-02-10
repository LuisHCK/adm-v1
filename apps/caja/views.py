
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import CajaForm
from .models import Caja


# Create your views here.
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
        if request.method == 'POST':
            form = CajaForm(request.POST)
            if form.is_valid():
                caja = form.save(commit=False)
                caja.usuario = request.user
                caja.save()
            return redirect('caja_inicio')
        else:
            form = CajaForm()
        return render(request, 'caja/saldo_form.html', {'form': form})


def cierre_caja(request):
    """Cierra caja y se retira el dinero"""
    ultima_caja = Caja.objects.last()
    if request.method == "POST":
        form = CajaForm(request.POST)
        if form.is_valid():
            caja = form.save(commit=False)
            caja.usuario = request.user
            caja.saldo = (ultima_caja.saldo - caja.saldo)
            caja.save()
            # Actualizar el saldo en caja
            ultima_caja.fecha_cierre = str(timezone.now())
            ultima_caja.save()
        return redirect('caja_inicio')
    else:
        form = CajaForm()
    return render(request, 'caja/saldo_form.html', {'form': form})
