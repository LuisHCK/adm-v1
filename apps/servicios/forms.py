
from django import forms
from django.forms import NumberInput, TextInput
from apps.servicios.models import Servicio


class ServicioForm(forms.ModelForm):
    """Formulario para los articulos"""
    class Meta:
        model = Servicio
        fields = ['descripcion', 'precio',]
        widgets = {
            'descripcion': TextInput(attrs={'class': 'form-control'}),
            'precio': NumberInput(attrs={'class': 'form-control'})
        }
