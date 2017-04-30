
from django import forms
from django.forms import TextInput, NumberInput, Select
from apps.inventario.models import Articulos, Inventario


class ArticuloForm(forms.ModelForm):
    """Formulario para los articulos"""
    class Meta:
        model = Articulos
        fields = ('codigo',
                  'nombre',
                  'descripcion',
                  'precio_compra',
                  'precio_venta',
                  'precio_venta2',
                  'precio_venta3',
                  'iva',
                  'cantidad_inicial')
        widgets = {
            'codigo': TextInput(attrs={'class': 'form-control'}),
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'descripcion': TextInput(attrs={'class': 'form-control'}),
            'precio_compra': NumberInput(attrs={'class': 'form-control'}),
            'precio_venta': NumberInput(attrs={'class': 'form-control'}),
            'precio_venta2': NumberInput(attrs={'class': 'form-control'}),
            'precio_venta3': NumberInput(attrs={'class': 'form-control'}),
            'iva': NumberInput(attrs={'class': 'form-control'}),
            'cantidad_inicial': NumberInput(attrs={'class': 'form-control'}),

        }
        labels = {
            'precio_venta': "Precio 1",
            'precio_venta2': "Precio 2",
            'precio_venta3': "Precio 3",
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
