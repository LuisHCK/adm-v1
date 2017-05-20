import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.common import validaciones

from .forms import CajaForm, EgresoForm
from .models import Caja, Capital, Egresos


@login_required(login_url='login') #redirect when user is not logged in

def inicio(request):
    """Muestra el estado actual de la caja"""
    ult = Caja.objects.last()
    ultima_caja_id = 0

    # Si la caja devuelve nulo evitar error en el template
    if ult:
        ultima_caja_id = ult.id
    else:
        ultima_caja_id = 0

    caja = Caja.objects.all().order_by('-fecha_apertura').exclude(id=ultima_caja_id)
    capital = Capital.objects.first()

    egresos = object
    # Si el el usuario es administrador podrá ver todas las solicitudes de egresos
    # Sólo se muestran las solicitudes que se realizan durante la caja esté abierta
    if validaciones.es_administrador(request.user):
        egresos = Egresos.objects.filter(caja=ult)
    else:
        egresos = Egresos.objects.filter(caja=ult, usuario=request.user)

    return render(request, 'caja/caja.html',
                  {'caja': caja,
                   'form_retiro': CajaForm,
                   'ultima_caja': ult,
                   'capital': capital,
                   'form_egreso': EgresoForm,
                   'egresos': egresos
                  })

def primera_apertura(request):
    '''Realiza la apertura inicial de la caja'''
    if request.method == 'POST' and validaciones.es_administrador(request.user):
        response_data = {}
        form = CajaForm(request.POST)

        if form.is_valid():
            caja = form.save(commit=False)
            caja.usuario = request.user
            caja.save()

            response_data['estado'] = str(caja.estado)
            response_data['fecha_apertura'] = str(caja.fecha_apertura)
            response_data['usuario'] = str(caja.usuario)
            response_data['saldo'] = str(caja.saldo)

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            response_data['result'] = 'El formulario no es válido.'
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json",
                status=500,
            )

    else:
        return HttpResponse(
            json.dumps({"error": "No estás autorizado para esta acción"}),
            content_type="application/json",
            status=500,
        )

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

def apertura_ajax(request, pk):
    '''Realiza apertura de caja mediante ajax'''
    response_data = {}
    if request.method == 'POST' and validaciones.es_administrador(request.user):
        caja_abierta = Caja.objects.get(pk=pk)

        #Si caja ya está abierta retornar un mensaje
        if caja_abierta.estado:
            response_data['result'] = 'La caja ya se encuentra abierta'
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
                )
        # En caso contrario realizar las operaciones de apertura
        else:
            caja_abierta.estado = True
            caja_abierta.fecha_apertura = str(timezone.now())
            caja_abierta.usuario = request.user
            caja_abierta.save()

            response_data['estado'] = str(caja_abierta.estado)
            response_data['fecha_apertura'] = str(caja_abierta.fecha_apertura)
            response_data['usuario'] = str(caja_abierta.usuario)
            response_data['saldo'] = str(caja_abierta.saldo)

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def cierre_caja(request):
    """Cierra caja y se retira el dinero"""
    ultima_caja = Caja.objects.last()
    if request.method == "POST":
        form = CajaForm(request.POST)
        if form.is_valid():
            caja = form.save(commit=False)
            caja.usuario = request.user

            # La ultima caja (la caja que estamos cerrando) debe reflejar el dinero ingresado
            # menos la cantidad que retiramos
            # Ejemplo Si entraron 1000 y retiramos 900 la ultima caja debere reflejar 900
            # entonces nuestro saldo inicial sería 100
            saldo_retiro = caja.saldo

            # Especifical el saldo que quedará en caja luego del retiro
            caja.saldo = (ultima_caja.saldo - caja.saldo)
            caja.save()

            # Restar de la caja el monto de retiro
            ultima_caja.saldo = saldo_retiro

            # Guardar el monto extrído en el Capital
            capital = Capital.objects.last()
            if capital:
                capital.monto = (capital.monto + caja.saldo)
                capital.save()
            else:
                Capital.objects.create(monto=caja.saldo)


            # Actualizar el saldo en caja
            ultima_caja.fecha_cierre = str(timezone.now())
            ultima_caja.save()
            messages.success(request, "Se realizó el cierre con éxito.")
        return redirect('caja_inicio')
    else:
        messages.error(request, "Ocurrió un error al realizar el cierre de caja.")
        form = CajaForm()
    return render(request, 'caja/saldo_form.html', {'form': form, 'ultima_caja': ultima_caja})


def estado_capital(request):
    """Mostar el capital con el que se cuenta"""
    capital = Capital.objects.first()
    ultima_caja = Caja.objects.last()
    caja = Caja.objects.exclude(id=ultima_caja.id).order_by('fecha_apertura')[:10]
    return render(request, 'capital/capital.html', {'capital': capital, 'caja': caja})


####### EGRESOS #######
def egreso_caja(request):
    '''Solicita un egreso de caja'''
    caja = Caja.objects.last()
    if request.method == "POST" and caja.estado:
        form = EgresoForm(request.POST)
        if form.is_valid():
            egreso = form.save(commit=False)
            egreso.usuario = request.user
            egreso.caja = caja
            egreso.save()

        messages.success(request, "Se realizó la solicitud de egreso")
        return redirect('caja_inicio')
    else:
        messages.error(request, "El formulario no es válido")
        form = EgresoForm()
    return redirect('caja_inicio')


def ver_egresos(request):
    """Muestra todos los egresos realizados"""
    egresos = Egresos.objects.all()
    return render(request, 'egresos/egresos.html', {'egresos': egresos})


def detalles_egreso(request, pk):
    """Ver detalles de un egreso"""
    egreso = get_object_or_404(Egresos, pk=pk)

    if egreso.estado == 'estado_aprovado' and egreso.cobrado is True:
        return render(request, 'egresos/detalles_egreso.html', {'egreso': egreso})
    else:
        raise Http404


def aprovar_egreso(request, pk, accion):
    if request.method == "POST" and validaciones.es_administrador(
            request.user):
        caja = Caja.objects.last()
        egreso = Egresos.objects.get(pk=pk)
        response_data = {}

        # Validar si el egreso es aprobable
        if egreso.cantidad < caja.saldo and accion == 'estado_aprovado' and egreso.estado == 'estado_pendiente' and caja.estado:
            egreso.aprovado_por = request.user
            egreso.estado = accion
            egreso.save()
            # Retornar la respuesta
            response_data['id'] = egreso.id
            response_data['aprovado_por'] = str(egreso.aprovado_por)
            # Retornar estado legible
            response_data['estado'] = str(egreso.estado)

            response_data['result'] = "El egreso fue Aprovado"
            return HttpResponse(
                json.dumps(response_data), content_type="application/json")
        # Validar que el monto a egresar no supere el estado en caja
        elif egreso.cantidad > caja.saldo and accion == 'estado_aprovado':
            response_data[
                'error'] = "La cantidad de egreso es mayor al saldo en caja."
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json",
                status=500)
        # Si una solicitud ya fue denegada no se puede volver a aprovar
        elif accion == 'estado_aprovado' and egreso.estado == 'estado_denegado':
            response_data['error'] = "El egreso ya no puede ser Aprovado"
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json",
                status=500)
        elif accion == 'estado_aprovado' and caja.estado is False:
            response_data[
                'error'] = "No se puede aprovar un egreso mientras la caja está cerrada"
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json",
                status=500)

        elif accion == 'estado_denegado':
            egreso.estado = accion
            egreso.save()

            response_data['id'] = egreso.id
            response_data['aprovado_por'] = str(egreso.aprovado_por)
            # Retornar estado legible
            response_data['estado'] = str(egreso.estado)

            response_data['result'] = "El egreso fue denegado"
            return HttpResponse(
                json.dumps(response_data), content_type="application/json")
        else:
            response_data[
                'error'] = "La solicitud no es válida, por favor revise los datos"
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json",
                status=500)
    else:
        return HttpResponse(
            json.dumps({
                "nothing_to_see": "nothing to see here :)"
            }),
            content_type="application/json")


def cobrar_egreso(request, pk):
    response_data = {}
    if request.method == "POST" and validaciones.es_cajero(request.user):
        egreso = Egresos.objects.get(pk=pk)
        caja = Caja.objects.last()

        if egreso.estado == "estado_aprovado" and egreso.caja == caja and egreso.cobrado is False:
            egreso.cobrado = True
            egreso.save()

            # Retirar el dinero de caja
            caja.saldo -= egreso.cantidad
            caja.save()

            response_data['result'] = "Se completó el egreso de: $"+str(egreso.cantidad)
            response_data['id'] = egreso.id
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json")

        # Si el egreso ha sido denegado no se puede cobrar
        elif egreso.estado == "estado_denegado":
            response_data['error'] = "No se puede cobrar un egreso Denegado"
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json",
                status=500)

        # El egreso no puede ser cobrado dos veces
        elif egreso.cobrado is True:
            response_data['error'] = "El egreso no se puede cobrar otra vez"
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json",
                status=500)

        # Si el egreso pertenece a una caja anterior ya no es válido
        elif egreso.caja != caja.id:
            response_data[
                'error'] = "La caja ya fue cerrada, el egreso ya no es válido"
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json",
                status=500)
        else:
            response_data['error'] = "La solicitud de egreso no es válida"
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json",
                status=500)

        # Si no se cumple ninguna de las condiciones, considerar la solicitud como inválida
    else:
        response_data['error'] = "La acción no es válida. Se requiere el Rol de Cajero"
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json",
            status=500)
