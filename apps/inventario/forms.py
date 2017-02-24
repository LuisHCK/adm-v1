
from django import forms
from django.forms import TextInput, NumberInput, Select
from apps.inventario.models import Articulos, Inventario


class ArticuloForm(forms.ModelForm):
    """Formulario para los articulos"""
    class Meta:
        model = Articulos
        fields = ('nombre', 'descripcion', 'precio_compra', 'precio_venta')
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'descripcion': TextInput(attrs={'class': 'form-control'}),
            'precio_compra': NumberInput(attrs={'class': 'form-control'}),
            'precio_venta': NumberInput(attrs={'class': 'form-control'}),
        }


class InventarioForm(forms.ModelForm):
    """Formulario de existencias en inventario"""
    class Meta:
        model = Inventario
        fields = ('articulo', 'existencias', 'minimo_existencias')
        widgets = {
            'articulo': Select(attrs={'class': 'form-control'}),
            'minimo_existencias': NumberInput(attrs={'class': 'form-control'}),
            'existencias': NumberInput(attrs={'class': 'form-control'}),
        }
