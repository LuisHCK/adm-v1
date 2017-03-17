from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm, PerfilForm, LoginForm, UserFormSettings
from .models import Perfil

# Esta view se encarga de comprobar las credenciales del usuario y asi iniciar sesion
def iniciar_sesion(request):
	if request.POST:
		login_form = LoginForm(request.POST)
		usuario = request.POST['username']
		passwd = request.POST['password']
		user = authenticate(username=usuario, password=passwd)
		if user is not None:
			login(request, user)		
			return redirect('inicio')
	else:		
		login_form = LoginForm()
	return render(request,'usuarios/iniciar_sesion.html', {'form': login_form})

# Esta view se encarga de cerrar la sesion actual
def cerrar_sesion(request):
	if request.POST:
		logout(request)
		return redirect('inicio')

# Esta view se encarga de crear una cuenta, comprobando que el nombre de usuario no exista y los campos sean correctos.
def crear_cuenta(request):
	if request.POST:
		user_form = UserForm(request.POST)
		if user_form.is_valid():			
			try:
				user = User.objects.get(username = request.POST["username"])
				return render(request, 'usuarios/crear_cuenta.html', {'form': user_form,'message': "El nombre de usuario ya existe."})

			except User.DoesNotExist:
				usuario = user_form.save()
				return redirect('inicio')

			else:
				return render(request, 'usuarios/crear_cuenta.html', {'form': user_form, 'message': "Las contraseñas no coiciden."})
		else:			
			return render(request, 'usuarios/crear_cuenta.html', {'form': user_form})


	else:
		user_form = UserForm()
		return render(request, 'usuarios/crear_cuenta.html', {'form': user_form})

# Esta view se encarga de cargar la configuracion actual del usuario usando los forms.
@login_required
def configuracion(request):
	current_user = User.objects.get(id=request.user.id)
	try:
		current_settings = Perfil.objects.get(usuario_id=current_user.id)
	except Perfil.DoesNotExist:
		Perfil.objects.create(usuario_id=current_user.id)
		current_settings = Perfil.objects.get(usuario_id=current_user.id)
	if request.POST:
		user_form = UserFormSettings(request.POST, instance=current_user)
		perfil_form = PerfilForm(request.POST, request.FILES, instance=current_settings)

		if user_form.is_valid() and perfil_form.is_valid():
			user_form.save()
			perfil_form.save()

			return redirect('inicio')

		else:
			return render(request, 'usuarios/configuracion.html', {
				'userform': user_form, 'perfilform': perfil_form
				})
	else:
		user_form = UserFormSettings(initial={'username': current_user.username,
			'first_name': current_user.first_name, 'last_name':current_user.last_name,
			'email':current_user.email})
		perfil_form = PerfilForm(initial={'cedula': current_settings.cedula,
			'puesto': current_settings.puesto, 'telefono': current_settings.telefono,
			'direccion': current_settings.direccion,
			'foto': current_settings.foto.url})
		foto = current_settings.foto
		return render(request, 'usuarios/configuracion.html', {
			'userform': user_form, 'perfilform': perfil_form, 'foto': foto
			})

