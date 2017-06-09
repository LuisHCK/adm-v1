
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Ajuste


class AjustesForm(forms.ModelForm):
    '''Form para realizar ajustes'''
    class Meta:
        model = Ajuste
        fields = ('name',
                  'direction',
                  'phone',
                  'email',
                  'simbolo_moneda',
                  'ruc',
                  'tipo_factura')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'direction': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'simbolo_moneda': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Simbolo Moneda'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Codigo RUC'}),
            'tipo_factura': forms.Select(attrs={'class': 'form-control'})
        }


class CloudForm(forms.ModelForm):
    class Meta:
        model = Ajuste
        fields = ('api_url', 'api_key')
        widgets = {
            'api_url': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Servidor de Sincronización'}),
            'api_key': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Llave de Acceso'}),
        }
        labels = {
            'api_url': _('Servidor'),
            'api_key': _('Llave de Acceso')
        }
