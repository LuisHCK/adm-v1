from django import forms
from .models import *

class AjustesForm(forms.ModelForm):
    '''Form para realizar ajustes'''
    class Meta:
        model = Ajuste
        fields = ('nombre', 'direccion', 'telefono', 'email', 'simbolo_moneda', 'ruc')
        widgets = {
            'nombre':forms.TextInput(attrs={'class': 'form-control'}),
            'direccion':forms.TextInput(attrs={'class': 'form-control'}),
            'telefono':forms.TextInput(attrs={'class': 'form-control'}),
            'email':forms.TextInput(attrs={'class': 'form-control'}),
            'simbolo_moneda':forms.TextInput(attrs={'class': 'form-control'}),
            'ruc':forms.TextInput(attrs={'class': 'form-control'})
            }
        