
from django import forms
from apps.inventario.models import Articulos, Inventario


class ArticuloForm(forms.ModelForm):
    """Formulario para los articulos"""
    class Meta:
        model = Articulos
        fields = ('nombre', 'descripcion', 'precio_compra', 'precio_venta')


class InventarioForm(forms.ModelForm):
    """Formulario de existencias en inventario"""
    class Meta:
        model = Inventario
        fields = ('articulo', 'existencias')
