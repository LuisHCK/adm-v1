
from django import forms
from django.forms import NumberInput, Select
from django.utils.translation import ugettext_lazy as _
from apps.ventas.models import Venta
from apps.servicios.models import Servicio


class VentaForm(forms.ModelForm):
    """Formulario para los articulos"""
    class Meta:
        model = Venta
        fields = ['articulo', 'cantidad', 'descuento']
        widgets = {
            'articulo': Select(attrs={'class': 'form-control'}),
            'cantidad': NumberInput(attrs={'class': 'form-control'}),
            'descuento': NumberInput(attrs={'class': 'form-control'})
        }


class ServicioForm(forms.ModelForm):
    """Formulario para los articulos"""
    class Meta:
        model = Servicio
        fields = ['tipo_servicio', 'cantidad']
        widgets = {
            'tipo_servicio': Select(attrs={'class': 'form-control'}),
            'cantidad': NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'articulo': _('Articulo (Opcional)'),
            'tipo_servicio': _('Tipo de Servicio realizado'),
        }
