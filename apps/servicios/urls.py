
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^nuevo/$', views.realizar_servicio, name='realizar_servicio'),
    url(r'^$', views.inicio, name='servicios_realizados'),
]