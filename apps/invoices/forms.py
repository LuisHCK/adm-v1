
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import TextInput, Select, NumberInput, RadioSelect
from .models import *


class InvoiceForm(forms.ModelForm):
    """Formulario de stocks en inventory"""
    class Meta:
        model = Invoice
        fields = ('client', 'payment_type')
        widgets = {
            'client': TextInput(attrs={'class': 'form-control'}),
            'payment_type': Select(attrs={'class': 'form-control'}),
        }


class InvoiceProductForm(forms.ModelForm):
    """Añadir items a la invoice"""
    class Meta:
        model = InvoiceProducts
        fields = ('product', 'quantity')
        widgets = {
            'product': Select(attrs={'class': 'form-control'}),
            'quantity': NumberInput(attrs={'class': 'form-control',}),
        }


class FastServiceForm(forms.ModelForm):
    """Formulario para los products"""
    class Meta:
        model = InvoiceServices

        fields = ['type_service', 'quantity']
        widgets = {
            'type_service': Select(attrs={'class': 'form-control',}),
            'quantity': NumberInput(attrs={
                'class': 'form-control',
                'id': 'cantidad_servicio'
                }),
        }
        labels = {
            'product': _('Articulo (Opcional)'),
            'type_service': _('Tipo de Service realizado'),
        }

