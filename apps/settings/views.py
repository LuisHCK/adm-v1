
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.common.validaciones import is_admin

from .forms import AjustesForm, CloudForm
from .models import Settings


@login_required(login_url='login')  # redirect when user is not logged in
def Start(request):
    settings = object
    form = object
    cloud_form = object

    if is_admin(request.user):
        try:
            settings = Settings.objects.get(pk=1)
            form = AjustesForm(request.POST or None, instance=settings)
            cloud_form = CloudForm(request.POST or None, instance=settings)

        except Settings.DoesNotExist:
            form = AjustesForm
            cloud_form = CloudForm()

        return render(request, 'settings/settings.html', {'form': form,
                                                        'cloud_form': cloud_form,
                                                        'settings': settings})
    else:
        messages.error(request, "No estas autorizado")
        return redirect('Start')


def guardar_ajustes(request):
    if request.method == "POST" and is_admin(request.user):
        # Crear un objeto vacio que almacenará los settings
        settings = object

        # Intentar obtener los settings desde la BD
        try:
            settings = Settings.objects.get(pk=1)

        # Crear el registro en caso de que no exista
        except Settings.DoesNotExist:
            Settings.objects.create(pk=1)
            settings = Settings.objects.get(pk=1)

        form = AjustesForm(request.POST or None, instance=settings)
        if form.is_valid():
            settings = form.save(commit=False)
            settings.save()

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
    if request.method == "POST" and is_admin(request.user):
        settings = object

        try:
            settings = Settings.objects.get(pk=1)
        except Settings.DoesNotExist:
            Settings.objects.create(pk=1)
            settings = Settings.objects.get(pk=1)

        form = CloudForm(request.POST or None, instance=settings)
        if form.is_valid():
            settings = form.save(commit=False)
            settings.save()

            messages.success(request, "Ajustes guardados con éxito")
            return redirect('inicio_ajustes')
        else:
            messages.error(request, "El formulario no es válido")
            return redirect('inicio_ajustes')
    else:
        messages.error(request, "Petición Incorrecta")
        return redirect('inicio_ajustes')
