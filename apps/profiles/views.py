import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Profile
from .forms import ProfileForm, UserForm

def admin_required(user):
    auth = False
    if user.groups.filter(name='Administrador').exists() or user.is_staff:
        auth = True
        return auth
    return auth


@login_required(login_url='login')  # redirect when user is not logged in
def ShowProfiles(request):
    '''Ver todos los profiles de usuarios'''
    if admin_required(request.user):
        profiles = Profile.objects.all()
        usuarios = User.objects.all()
        return render(request, 'profiles/profiles.html',
        {'profiles': profiles, 'usuarios': usuarios})
    else:
        messages.error(request, "Permisos Insuficientes. Error 0x01")
        return redirect('Start')


def ShowProfile(request, pk):
    '''Ver detalles de un Profile'''
    if admin_required(request.user):
        profile = get_object_or_404(Profile, pk=pk)
        form = ProfileForm(request.POST or None, instance=profile)
        form_usr = UserForm(request.POST or None, instance=profile.user)

        position = None
        try:
            position = str(profile.user.groups.all()[0])
        except IndexError:
            position = "No definido"
            messages.error(request, "No se ha defindo el cargo para "+ str(profile) +". Error 0x01")

        return render(request, 'profiles/profile.html', {
            'profile': profile,
            'position': position,
            'form': form,
            'form_usr': form_usr,
            })
    else:
        messages.error(request, "Permisos Insuficientes. Error 0x01")
        return redirect('Start')

def EditProfiles(request, pk):
    '''Edita el profile de un user'''
    position = "No definido"
    if admin_required(request.user):
        profile = get_object_or_404(Profile, pk=pk)

        try:
            position = str(profile.user.groups.all()[0])
        except IndexError:
            print("Index Error")

        form = ProfileForm(request.POST or None, request.FILES, instance=profile)
        if request.method == 'POST' and form.is_valid():
            form.save()

            return redirect('ShowProfile', profile.id)

        else:
            return render(request, 'profiles/profile.html', {
                'profile': profile,
                'position': position,
                'form': form
            })
    else:
        messages.error(request, "Permisos Insuficientes. Error 0x01")
        return redirect('Start')
