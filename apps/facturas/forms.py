
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import TextInput, Select, NumberInput, RadioSelect
from .models import *


class FacturaForm(forms.ModelForm):
    """Formulario de existencias en inventario"""
    class Meta:
        model = Factura
        fields = ('cliente', 'pago')
        widgets = {
            'cliente': TextInput(attrs={'class': 'form-control'}),
            'pago': Select(attrs={'class': 'form-control'}),
        }


class FacturaArticuloForm(forms.ModelForm):
    """Añadir items a la factura"""
    class Meta:
        model = FacturaArticulos
        fields = ('articulo', 'cantidad')
        widgets = {
            'articulo': Select(attrs={'class': 'form-control'}),
            'cantidad': NumberInput(attrs={'class': 'form-control',}),
        }


class ServicioRapidoForm(forms.ModelForm):
    """Formulario para los articulos"""
    class Meta:
        model = FacturaServicios

        fields = ['tipo_servicio', 'cantidad']
        widgets = {
            'tipo_servicio': Select(attrs={'class': 'form-control',}),
            'cantidad': NumberInput(attrs={
                'class': 'form-control',
                'id': 'cantidad_servicio'
                }),
        }
        labels = {
            'articulo': _('Articulo (Opcional)'),
            'tipo_servicio': _('Tipo de Servicio realizado'),
        }

