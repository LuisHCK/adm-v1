
from django import forms
from apps.ventas.models import Venta


class VentaForm(forms.ModelForm):
    """Formulario para los articulos"""
    class Meta:
        model = Venta
        fields = ('articulo', 'cantidad', 'descuento')
