
from django import forms
from django.forms import TextInput, Select, NumberInput
from .models import Factura, FacturaItems


class FacturaForm(forms.ModelForm):
    """Formulario de existencias en inventario"""
    class Meta:
        model = Factura
        fields = ('cliente', 'cobrada')
        widgets = {
            'cliente': TextInput(attrs={'class': 'form-control'}),
            'cobrada': Select(choices={(True, 'Cobrado'), (False, 'Sin Cobrar')}, attrs={'class': 'form-control'}),
        }


class ItemsForm(forms.ModelForm):
    """Añadir items a la factura"""
    class Meta:
        model = FacturaItems
        fields = ('concepto', 'precio')
        widgets = {
            'concepto': TextInput(attrs={'class': 'form-control'}),
            'precio': NumberInput(attrs={'class': 'form-control'}),
        }
