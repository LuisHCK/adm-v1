
from django.contrib import messages
from django.shortcuts import redirect, render

from apps.common.validaciones import es_administrador

from .forms import AjustesForm, CloudForm
from .models import Ajuste


def inicio(request):
    ajustes = object
    form = object
    cloud_form = object

    try:
        ajustes = Ajuste.objects.get(pk=1)
        form = AjustesForm(request.POST or None, instance=ajustes)
        cloud_form = CloudForm(request.POST or None, instance=ajustes)

    except Ajuste.DoesNotExist:
        form = AjustesForm
        cloud_form = CloudForm()

    return render(request, 'ajustes/ajustes.html', {'form': form,
                                                    'cloud_form': cloud_form,
                                                    'ajustes': ajustes})


def guardar_ajustes(request):
    if request.method == "POST" and es_administrador(request.user):
        # Crear un objeto vacio que almacenará los ajustes
        ajustes = object

        # Intentar obtener los ajustes desde la BD
        try:
            ajustes = Ajuste.objects.get(pk=1)

        # Crear el registro en caso de que no exista
        except Ajuste.DoesNotExist:
            Ajuste.objects.create(pk=1)
            ajustes = Ajuste.objects.get(pk=1)

        form = AjustesForm(request.POST or None, instance=ajustes)
        if form.is_valid():
            ajustes = form.save(commit=False)
            ajustes.save()

            messages.success(request, "Ajustes guardados con éxito")
            return redirect('inicio_ajustes')
        else:
            messages.error(request, "El formulario no es válido")
            return redirect('inicio_ajustes')
    else:
        messages.error(request, "El formulario no es válido")
        return redirect('inicio_ajustes')

# Básicamente el mismo método anterior, pero con un un form distinto}
# Mientras averiguo como hacerlo con un solo metodo
def guardar_cloud(request):
    if request.method == "POST" and es_administrador(request.user):
        ajustes = object

        try:
            ajustes = Ajuste.objects.get(pk=1)
        except Ajuste.DoesNotExist:
            Ajuste.objects.create(pk=1)
            ajustes = Ajuste.objects.get(pk=1)

        form = CloudForm(request.POST or None, instance=ajustes)
        if form.is_valid():
            ajustes = form.save(commit=False)
            ajustes.save()

            messages.success(request, "Ajustes guardados con éxito")
            return redirect('inicio_ajustes')
        else:
            messages.error(request, "El formulario no es válido")
            return redirect('inicio_ajustes')
    else:
        messages.error(request, "Petición Incorrecta")
        return redirect('inicio_ajustes')
