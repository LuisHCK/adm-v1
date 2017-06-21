import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.common import validaciones

from .forms import CajaForm, EgresoForm
from .models import Cash, Money, Expenses


@login_required(login_url='login') #redirect when user is not logged in

def Start(request):
    """Muestra el status actual de la cash"""
    ult = Cash.objects.last()
    last_cash_id = 0

    # Si la cash devuelve nulo evitar error en el template
    if ult:
        last_cash_id = ult.id
    else:
        last_cash_id = 0

    cash = Cash.objects.all().order_by('-opening_date').exclude(id=last_cash_id)
    capital = Money.objects.first()

    egresos = object
    # Si el el user es administrador podrá ver todas las solicitudes de egresos
    # Sólo se muestran las solicitudes que se realizan durante la cash esté abierta
    if validaciones.is_admin(request.user):
        egresos = Expenses.objects.filter(cash=ult)
    else:
        egresos = Expenses.objects.filter(cash=ult, user=request.user)

    return render(request, 'cash/cash.html',
                  {'cash': cash,
                   'form_retiro': CajaForm,
                   'last_cash': ult,
                   'capital': capital,
                   'form_egreso': EgresoForm,
                   'egresos': egresos
                  })

def primera_apertura(request):
    '''Realiza la apertura inicial de la cash'''
    if request.method == 'POST' and validaciones.is_admin(request.user):
        response_data = {}
        form = CajaForm(request.POST)

        if form.is_valid():
            cash = form.save(commit=False)
            cash.user = request.user
            cash.save()

            response_data= {
                'status': str(cash.status)
                'opening_date': str(cash.opening_date)
                'user': str(cash.user)
                'balance': str(cash.balance)
            }

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
    """Abre el uso de la cash"""
    cash = Cash.objects.last()
    if cash:
        return redirect('caja_inicio')
    else:
        if request.method == 'POST' and validaciones.is_admin(request.user):
            form = CajaForm(request.POST)
            if form.is_valid():
                cash = form.save(commit=False)
                cash.user = request.user
                cash.save()
            messages.success(request, "Se realizó la apertura.")
            return redirect('caja_inicio')
        else:
            form = CajaForm()
        return render(request, 'cash/saldo_form.html', {'form': form})

def apertura_ajax(request, pk):
    '''Realiza apertura de cash mediante ajax'''
    response_data = {}
    if request.method == 'POST' and validaciones.is_admin(request.user):
        caja_abierta = Cash.objects.get(pk=pk)

        #Si cash ya está abierta retornar un mensaje
        if caja_abierta.status:
            response_data['result'] = 'La cash ya se encuentra abierta'
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
                )
        # En caso contrario realizar las operaciones de apertura
        else:
            caja_abierta.status = True
            caja_abierta.opening_date = str(timezone.now())
            caja_abierta.user = request.user
            caja_abierta.save()

            response_data['status'] = str(caja_abierta.status)
            response_data['opening_date'] = str(caja_abierta.opening_date)
            response_data['user'] = str(caja_abierta.user)
            response_data['balance'] = str(caja_abierta.balance)

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
    """Cierra cash y se retira el dinero"""
    last_cash = Cash.objects.last()
    if request.method == "POST":
        form = CajaForm(request.POST)
        if form.is_valid():
            cash = form.save(commit=False)
            cash.user = request.user

            # La ultima cash (la cash que estamos cerrando) debe reflejar el dinero ingresado
            # menos la quantity que retiramos
            # Ejemplo Si entraron 1000 y retiramos 900 la ultima cash debere reflejar 900
            # entonces nuestro balance inicial sería 100
            saldo_retiro = cash.balance

            # Especifical el balance que quedará en cash luego del retiro
            cash.balance = (last_cash.balance - cash.balance)
            cash.save()

            # Restar de la cash el monto de retiro
            last_cash.balance = saldo_retiro

            # Guardar el monto extrído en el Money
            capital = Money.objects.last()
            if capital:
                capital.monto = (capital.monto + cash.balance)
                capital.save()
            else:
                Money.objects.create(monto=cash.balance)


            # Actualizar el balance en cash
            last_cash.closing_date = str(timezone.now())
            last_cash.save()
            messages.success(request, "Se realizó el cierre con éxito.")
        return redirect('caja_inicio')
    else:
        messages.error(request, "Ocurrió un error al realizar el cierre de cash.")
        form = CajaForm()
    return render(request, 'cash/saldo_form.html', {'form': form, 'last_cash': last_cash})


def estado_capital(request):
    """Mostar el capital con el que se cuenta"""
    capital = Money.objects.first()
    last_cash = Cash.objects.last()
    cash = Cash.objects.exclude(id=last_cash.id).order_by('opening_date')[:10]
    return render(request, 'capital/capital.html', {'capital': capital, 'cash': cash})


####### EGRESOS #######
def egreso_caja(request):
    '''Solicita un egreso de cash'''
    cash = Cash.objects.last()
    response_data = {}
    if request.method == "POST" and cash.status:
        form = EgresoForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.cash = cash
            expense.save()

            response_data = {
                'result': str('Solicitud enviada'),
                'quantity': str(expense.quantity),
                'details': str(expense.details),
                'user': str(expense.user),
                'status': str(expense.status),
                'approved_by': str(expense.approved_by),
                'charged': str(expense.charged),
                'expense_date': str(expense.expense_date),
            }
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    else:
        messages.error(request, "El formulario no es válido")
        form = EgresoForm()
    return HttpResponse(
                json.dumps({"result": "nothing to see"}),
                content_type="application/json",
                status=500
            )


def ver_egresos(request):
    """Muestra todos los egresos realizados"""
    egresos = Expenses.objects.all()
    return render(request, 'egresos/egresos.html', {'egresos': egresos})


def detalles_egreso(request, pk):
    """Ver detalles de un egreso"""
    egreso = get_object_or_404(Expenses, pk=pk)

    if egreso.status == 'estado_aprovado' and egreso.charged is True:
        return render(request, 'egresos/detalles_egreso.html', {'egreso': egreso})
    else:
        raise Http404


def aprovar_egreso(request, pk, accion):
    if request.method == "POST" and validaciones.is_admin(
            request.user):
        cash = Cash.objects.last()
        egreso = Expenses.objects.get(pk=pk)
        response_data = {}

        # Validar si el egreso es aprobable
        if egreso.quantity < cash.balance and accion == 'estado_aprovado' and egreso.status == 'estado_pendiente' and cash.status:
            egreso.approved_by = request.user
            egreso.status = accion
            egreso.save()
            # Retornar la respuesta
            response_data['id'] = egreso.id
            response_data['approved_by'] = str(egreso.approved_by)
            # Retornar status legible
            response_data['status'] = str(egreso.status)

            response_data['result'] = "El egreso fue Aprovado"
            return HttpResponse(
                json.dumps(response_data), content_type="application/json")
        # Validar que el monto a egresar no supere el status en cash
        elif egreso.quantity > cash.balance and accion == 'estado_aprovado':
            response_data[
                'error'] = "La quantity de egreso es mayor al balance en cash."
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json",
                status=500)
        # Si una solicitud ya fue denegada no se puede volver a aprovar
        elif accion == 'estado_aprovado' and egreso.status == 'estado_denegado':
            response_data['error'] = "El egreso ya no puede ser Aprovado"
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json",
                status=500)
        elif accion == 'estado_aprovado' and cash.status is False:
            response_data[
                'error'] = "No se puede aprovar un egreso mientras la cash está closed"
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json",
                status=500)

        elif accion == 'estado_denegado':
            egreso.status = accion
            egreso.save()

            response_data['id'] = egreso.id
            response_data['approved_by'] = str(egreso.approved_by)
            # Retornar status legible
            response_data['status'] = str(egreso.status)

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
        egreso = Expenses.objects.get(pk=pk)
        cash = Cash.objects.last()

        if egreso.status == "estado_aprovado" and egreso.cash == cash and egreso.charged is False:
            egreso.charged = True
            egreso.save()

            # Retirar el dinero de cash
            cash.balance -= egreso.quantity
            cash.save()

            response_data['result'] = "Se completó el egreso de: $"+str(egreso.quantity)
            response_data['id'] = egreso.id
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json")

        # Si el egreso ha sido denegado no se puede cobrar
        elif egreso.status == "estado_denegado":
            response_data['error'] = "No se puede cobrar un egreso Denegado"
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json",
                status=500)

        # El egreso no puede ser charged dos veces
        elif egreso.charged is True:
            response_data['error'] = "El egreso no se puede cobrar otra vez"
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json",
                status=500)

        # Si el egreso pertenece a una cash anterior ya no es válido
        elif egreso.cash != cash.id:
            response_data[
                'error'] = "La cash ya fue closed, el egreso ya no es válido"
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
