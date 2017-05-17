from django.shortcuts import render, redirect
from .forms import AjustesForm

def inicio(request):

    return render(request, 'ajustes/ajustes.html', {'form': AjustesForm})
