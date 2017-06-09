import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Perfil
from .forms import FormPerfil, UserForm

def admin_required(user):
    auth = False
    if user.groups.filter(name='Administrador').exists() or user.is_staff:
        auth = True
        return auth
    return auth


@login_required(login_url='login')  # redirect when user is not logged in
def ver_perfiles(request):
    '''Ver todos los perfiles de usuarios'''
    if admin_required(request.user):
        perfiles = Perfil.objects.all()
        usuarios = User.objects.all()
        return render(request, 'perfiles/perfiles.html',
        {'perfiles': perfiles, 'usuarios': usuarios})
    else:
        messages.error(request, "Permisos Insuficientes. Error 0x01")
        return redirect('inicio')


def ver_perfil(request, pk):
    '''Ver detalles de un Perfil'''
    if admin_required(request.user):
        perfil = get_object_or_404(Perfil, pk=pk)
        form = FormPerfil(request.POST or None, instance=perfil)
        form_usr = UserForm(request.POST or None, instance=perfil.user)

        puesto = None
        try:
            puesto = str(perfil.user.groups.all()[0])
        except IndexError:
            puesto = "No definido"
            messages.error(request, "No se ha defindo el cargo para "+ str(perfil) +". Error 0x01")

        return render(request, 'perfiles/perfil.html', {
            'perfil': perfil,
            'puesto': puesto,
            'form': form,
            'form_usr': form_usr,
            })
    else:
        messages.error(request, "Permisos Insuficientes. Error 0x01")
        return redirect('inicio')

def editar_perfil(request, pk):
    '''Edita el perfil de un user'''
    puesto = "No definido"
    if admin_required(request.user):
        perfil = get_object_or_404(Perfil, pk=pk)

        try:
            puesto = str(perfil.user.groups.all()[0])
        except IndexError:
            print("Index Error")

        form = FormPerfil(request.POST or None, request.FILES, instance=perfil)
        if request.method == 'POST' and form.is_valid():
            form.save()

            return redirect('ver_perfil', perfil.id)

        else:
            return render(request, 'perfiles/perfil.html', {
                'perfil': perfil,
                'puesto': puesto,
                'form': form
            })
    else:
        messages.error(request, "Permisos Insuficientes. Error 0x01")
        return redirect('inicio')
