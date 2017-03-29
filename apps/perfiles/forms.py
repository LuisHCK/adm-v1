from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django import forms
from .models import Perfil

'''Formulario para Editar y Crear Perfiles'''
class FormPerfil(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = (
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
			'nombres': 'Nombres Completos',
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

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password')
		widgets = {
			'username': forms.TextInput(attrs={'class': 'form-control input-lg', 'placeholder': ''}),
			'first_name': forms.TextInput(attrs={'class': 'form-control input-lg', 'placeholder': ''}),
			'last_name': forms.TextInput(attrs={'class': 'form-control input-lg', 'placeholder': ''}),
			'email': forms.TextInput(attrs={'class': 'form-control input-lg', 'placeholder': ''}),
			'password': forms.PasswordInput(attrs={'class': 'form-control input-lg', 'placeholder': ''}),

		}
		help_texts = {
			'username': None,
		}
		labels = {
			'first_name' : 'Nombre',
			'last_name' : 'Apellido',
			'username': 'Nombre de usuario',
			'email' : 'Correo Electronico',
			'password' : 'Contraseña',
		}
	confirmar_passwd = forms.CharField(widget=forms.PasswordInput(attrs={
		'class': 'form-control input-lg'
		}))

	#Este metodo se encarga de limpiar y determinar si las contraseñas ingresadas son iguales
	def clean(self):
		cleaned_data = self.cleaned_data
		pass1 = cleaned_data.get("password")
		pass2 = cleaned_data.get("confirmar_passwd")
		if pass1 != pass2:
			raise forms.ValidationError("Las contraseñas no coiciden.")
		return cleaned_data

	def save(self, commit=True):
		user = super(UserForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user
