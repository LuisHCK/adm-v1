from django import forms
from .models import Perfil

'''Formulario para Editar y Crear Perfiles'''
class FormPerfil(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = (
            'usuario',
            'nombres',
            'apellidos',
            'cedula',
            'direccion',
            'email',
            'telefono',
            'fecha_nacimiento',
            'fecha_entrada',
            'fecha_salida',
            'foto',
            )
        widgets = {
            'usuario':forms.Select(attrs={'class': 'form-control',}),
            'nombres':forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos':forms.TextInput(attrs={'class': 'form-control'}),
            'cedula':forms.TextInput(attrs={'class': 'form-control'}),
            'direccion':forms.TextInput(attrs={'class': 'form-control'}),
            'email':forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono':forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento':forms.DateInput(attrs={'class': 'form-control'}),
            'fecha_entrada':forms.DateInput(attrs={'class': 'form-control'}),
            'fecha_salida':forms.DateInput(attrs={'class': 'form-control'}),
            'foto':forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'usuario': 'Usuario',
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'cedula': 'Cédula de Identidad',
            'direccion': 'Dirección de recidencia',
            'email': 'Correo Electrónico',
            'telefono': 'Número de teléfono',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'fecha_entrada': 'Fecha de entrada',
            'fecha_salida': 'Fecha de Salida',
            'foto': 'Foto',
        }