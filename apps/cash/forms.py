
from django import forms
from django.forms import NumberInput, TextInput
from .models import Cash, Expenses
from django.utils.translation import ugettext_lazy as _


class CajaForm(forms.ModelForm):
    """Formulario para cirre y apartura de cash"""
    class Meta:
        model = Cash
        fields = ('balance',)
        widgets = {
            'balance': NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'balance': _('Cantidad a a Retirar de cash'),
        }

class EgresoForm(forms.ModelForm):
    """Formulario para el retiro de dinero de la cash abierta"""
    class Meta:
        model = Expenses
        fields = ('quantity', 'details',)
        widgets = {
            'quantity': NumberInput(attrs={'class': 'form-control'}),
            'details': TextInput(attrs={'class': 'form-control'})
        }
