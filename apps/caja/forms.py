
from django import forms
from django.forms import NumberInput
from .models import Caja
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
