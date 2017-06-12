
from django import forms
from django.forms import NumberInput, Select
from django.utils.translation import ugettext_lazy as _
from apps.sales.models import Sale
from apps.services.models import Service


class SaleForm(forms.ModelForm):
    """Formulario para los products"""
    class Meta:
        model = Sale
        fields = ['product', 'quantity']
        widgets = {
            'product': Select(attrs={'class': 'form-control'}),
            'quantity': NumberInput(attrs={'class': 'form-control', 'id': 'cantidad_articulo'}),
        }


class ServiceForm(forms.ModelForm):
    """Formulario para los products"""
    class Meta:
        model = Service
        fields = ['type_service', 'quantity']
        widgets = {
            'type_service': Select(attrs={'class': 'form-control'}),
            'quantity': NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'product': _('Articulo (Opcional)'),
            'type_service': _('Tipo de Service realizado'),
        }
