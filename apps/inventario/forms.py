
from django import forms
from django.forms import TextInput, NumberInput, Select, CheckboxInput
from apps.inventario.models import Product, Inventory


class ArticuloForm(forms.ModelForm):
    """Formulario para los articulos"""
    class Meta:
        model = Product
        fields = ('code',
                  'name',
                  'description',
                  'purchase_price',
                  'sale_price',
                  'sale_price2',
                  'sale_price3',
                  'iva',
                  'initial_ammount')
        widgets = {
            'code': TextInput(attrs={'class': 'form-control'}),
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control'}),
            'purchase_price': NumberInput(attrs={'class': 'form-control'}),
            'sale_price': NumberInput(attrs={'class': 'form-control'}),
            'sale_price2': NumberInput(attrs={'class': 'form-control'}),
            'sale_price3': NumberInput(attrs={'class': 'form-control'}),
            'iva': NumberInput(attrs={'class': 'form-control'}),
            'initial_ammount': NumberInput(attrs={'class': 'form-control'}),

        }
        labels = {
            'sale_price': "Precio 1",
            'sale_price2': "Precio 2",
            'sale_price3': "Precio 3",
        }


class InventarioForm(forms.ModelForm):
    """Formulario de stocks en inventario"""
    class Meta:
        model = Inventory
        fields = ('product', 'stocks', 'min_stocks', 'active')
        widgets = {
            'product': Select(attrs={'class': 'form-control'}),
            'min_stocks': NumberInput(attrs={'class': 'form-control'}),
            'stocks': NumberInput(attrs={'class': 'form-control'}),
            'active': CheckboxInput(attrs={'class': 'form-control'}),
        }
