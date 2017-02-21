
from django import forms
from django.forms import TextInput, Select, NumberInput
from .models import *


class FacturaForm(forms.ModelForm):
    """Formulario de existencias en inventario"""
    class Meta:
        model = Factura
        fields = ('cliente', 'cobrada')
        widgets = {
            'cliente': TextInput(attrs={'class': 'form-control'}),
            'cobrada': Select(choices={(True, 'Cobrado'), (False, 'Sin Cobrar')}, attrs={'class': 'form-control'}),
        }


class FacturaArticuloForm(forms.ModelForm):
    """Añadir items a la factura"""
    class Meta:
        model = FacturaArticulos
        fields = ('articulo', 'cantidad')
        widgets = {
            'articulo': Select(attrs={'class': 'form-control'}),
            'cantidad': NumberInput(attrs={'class': 'form-control'}),
        }
