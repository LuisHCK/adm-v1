
from django import forms
from django.forms import Select, NumberInput
from apps.sales.models import Sale


class SaleForm(forms.ModelForm):
    """Formulario para los products"""
    class Meta:
        model = Sale
        fields = ('product', 'quantity', 'discount')
        widgets = {
            'product': Select(attrs={'class': 'form-control'}),
            'quantity': NumberInput(attrs={'class': 'form-control'}),
            'discount': NumberInput(attrs={'class': 'form-control'}),
        }
