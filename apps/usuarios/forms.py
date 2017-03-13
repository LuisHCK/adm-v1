from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .models import Perfil

''' Forms para registro
'''

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ( 'username','first_name', 'last_name','email', 'password')
		widgets = {
			'username': forms.TextInput(attrs={'class': 'form-control input-lg', 'placeholder': ''}),
			'first_name': forms.TextInput(attrs={'class': 'form-control input-lg','placeholder': ''}),
			'last_name': forms.TextInput(attrs={'class': 'form-control input-lg','placeholder': ''}),
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
	confirmar_passwd = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-lg'}))

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

class PerfilForm(forms.ModelForm):
	class Meta:
		model = Perfil
		fields = ('cedula', 'puesto', 'telefono', 'direccion', 'foto')
		widgets = {
			'cedula': forms.TextInput(attrs={'class': 'form-control'}),
			'puesto': forms.TextInput(attrs={'class': 'form-control'}),			
			'telefono': forms.TextInput(attrs={'class': 'form-control'}),
			'direccion': forms.TextInput(attrs={'class': 'form-control'}),
			'foto': forms.ClearableFileInput(),
		}
		labels = {
			'cedula': 'Cédula',
			'puesto': 'Puesto',			
			'telefono': 'Teléfono',
			'direccion': 'Dirección actual',
			'foto': 'Foto Personal',
		}

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())

class UserFormSettings(UserForm):
	def __init__(self, *args, **kwargs):
		super(UserFormSettings, self).__init__(*args, **kwargs)
		self.fields.pop('password')
		self.fields.pop('confirmar_passwd')

	def clean(self):
		cleaned_data = super(UserFormSettings, self).clean()     
		return cleaned_data
	
	def save(self, commit=True):
		pass
