from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django import forms
from .models import Profile

'''Formulario para Editar y Crear Perfiles'''
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
			'name',
			'last_name',
            'identification_card',
            'direction',
            'email',
            'phone',
            'birthdate',
            'start_date',
            'depurate_date',
            'picture',
            )
        widgets = {
            'name':forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':forms.TextInput(attrs={'class': 'form-control'}),
            'identification_card':forms.TextInput(attrs={'class': 'form-control'}),
            'direction':forms.TextInput(attrs={'class': 'form-control'}),
            'email':forms.EmailInput(attrs={'class': 'form-control'}),
            'phone':forms.TextInput(attrs={'class': 'form-control'}),
            'birthdate':forms.DateInput(attrs={'class': 'form-control'}),
            'start_date':forms.DateInput(attrs={'class': 'form-control'}),
            'depurate_date':forms.DateInput(attrs={'class': 'form-control'}),
            'picture':forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
			'name': 'Nombres Completos',
			'last_name': 'Apellidos',
            'identification_card': 'Cédula de Identidad',
            'direction': 'Dirección de recidencia',
            'email': 'Correo Electrónico',
            'phone': 'Número de teléfono',
            'birthdate': 'Fecha de Nacimiento',
            'start_date': 'Fecha de entrada',
            'depurate_date': 'Fecha de Salida',
            'picture': 'Foto',
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
			'username': 'Nombre de user',
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
