
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import NumberInput, TextInput, Select
from apps.servicios.models import Servicio, TipoServicio


class ServicioForm(forms.ModelForm):
    """Formulario para los articulos"""
    class Meta:
        model = Servicio

        fields = ['tipo_servicio', 'precio', 'cantidad']
        widgets = {
            'tipo_servicio': Select(attrs={'class': 'form-control'}),
            'articulo': Select(attrs={'class': 'form-control'}),
            'cantidad': NumberInput(attrs={'class': 'form-control'}),
            'precio': NumberInput(attrs={'class': 'form-control'})
        }
        labels = {
            'articulo': _('Articulo (Opcional)'),
            'tipo_servicio': _('Tipo de Servicio realizado'),
        }
