
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.inicio, name='inicio'),
    url(r'^venta_rapida/$', views.venta_ajax, name='venta_ajax'),
    url(r'^servicio_rapido/$', views.servicio_ajax, name='servicio_ajax'),
]
