
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import NumberInput, TextInput, Select
from apps.services.models import Service, TypeService


class ServiceForm(forms.ModelForm):
    """Formulario para los products"""
    class Meta:
        model = Service

        fields = ['type_service', 'quantity']
        widgets = {
            'type_service': Select(attrs={'class': 'form-control'}),
            'quantity': NumberInput(attrs={'class': 'form-control', 'id': 'cantidad_servicio'}),
        }
        labels = {
            'product': _('Articulo (Opcional)'),
            'type_service': _('Tipo de Service realizado'),
        }

class TipoServicioForm(forms.ModelForm):
    '''Formulario para crear tipos de serivicio'''
    class Meta:
        model = TypeService

        fields = ['name', 'code', 'price']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'code': TextInput(attrs={'class': 'form-control'}),
            'price': NumberInput(attrs={'class': 'form-control'}),
        }
