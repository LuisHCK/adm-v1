
from django import forms
from django.forms import NumberInput, TextInput
from .models import Caja, Egresos
from django.utils.translation import ugettext_lazy as _


class CajaForm(forms.ModelForm):
    """Formulario para cirre y apartura de caja"""
    class Meta:
        model = Caja
        fields = ('saldo',)
        widgets = {
            'saldo': NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'saldo': _('Cantidad a a Retirar de caja'),
        }

class EgresoForm(forms.ModelForm):
    """Formulario para el retiro de dinero de la caja abierta"""
    class Meta:
        model = Egresos
        fields = ('cantidad', 'concepto',)
        widgets = {
            'cantidad': NumberInput(attrs={'class': 'form-control'}),
            'concepto': TextInput(attrs={'class': 'form-control'})
        }
