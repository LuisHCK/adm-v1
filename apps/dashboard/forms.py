
from django import forms
from django.forms import NumberInput, Select
from apps.ventas.models import Venta


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
