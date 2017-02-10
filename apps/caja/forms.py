
from django import forms
from .models import Caja

class CajaForm(forms.ModelForm):
    """Formulario para cirre y apartura de caja"""
    class Meta:
        model = Caja
        fields = ('saldo',)
