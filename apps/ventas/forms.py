
from django import forms
from django.forms import Select, NumberInput
from apps.ventas.models import Sale


class VentaForm(forms.ModelForm):
    """Formulario para los articulos"""
    class Meta:
        model = Sale
        fields = ('product', 'quantity', 'discount')
        widgets = {
            'product': Select(attrs={'class': 'form-control'}),
            'quantity': NumberInput(attrs={'class': 'form-control'}),
            'discount': NumberInput(attrs={'class': 'form-control'}),
        }
