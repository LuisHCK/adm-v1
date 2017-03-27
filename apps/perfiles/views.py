from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Perfil
from .forms import FormPerfil

@login_required(login_url='login')  # redirect when user is not logged in

def ver_perfiles(request):
    '''Ver todos los perfiles de usuarios'''
    perfiles = Perfil.objects.all()
    usuarios = User.objects.all()
    return render(request, 'perfiles/perfiles.html', {'perfiles':perfiles, 'usuarios':usuarios})

def editar_perfil(request, usuario):
    '''Edita el perfil de un usuario'''
    perfil = Perfil.objects.get(usuario_id=usuario)
    response_data = {}

    form = FormPerfil(request.POST or None, instance=perfil)
    if request.method == 'POST' and form.is_valid():
        form.save()

        return redirect('perfiles')

    return render(request, 'perfiles/editar.html', {
        'form': form
    })
