
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import NumberInput, TextInput, Select
from apps.servicios.models import Servicio


class ServicioForm(forms.ModelForm):
    """Formulario para los articulos"""
    class Meta:
        model = Servicio
        fields = ['descripcion', 'precio', 'articulo', 'articulos_cantidad']
        widgets = {
            'descripcion': TextInput(attrs={'class': 'form-control'}),
            'articulo': Select(attrs={'class': 'form-control'}),
            'articulos_cantidad': NumberInput(attrs={'class': 'form-control'}),
            'precio': NumberInput(attrs={'class': 'form-control'})
        }
        labels = {
            'articulo': _('Articulo (Opcional)'),
        }
