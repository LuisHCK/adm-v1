
from django import forms
from django.forms import NumberInput, Select
from django.utils.translation import ugettext_lazy as _
from apps.ventas.models import Venta
from apps.servicios.models import Servicio


class VentaForm(forms.ModelForm):
    """Formulario para los articulos"""
    class Meta:
        model = Venta
        fields = ['articulo', 'cantidad']
        widgets = {
            'articulo': Select(attrs={'class': 'form-control'}),
            'cantidad': NumberInput(attrs={'class': 'form-control', 'id': 'cantidad_articulo'}),
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
