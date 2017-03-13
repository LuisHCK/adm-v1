from django.conf.urls import url
from . import views

app_name = 'usuarios'
urlpatterns = [
	url(r'^registrarse/', views.crear_cuenta, name = 'registrar_usuario'),
	url(r'^logearse/', views.iniciar_sesion, name = 'iniciar_sesion'),
]