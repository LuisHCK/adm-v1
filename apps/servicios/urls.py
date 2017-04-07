
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^nuevo/$', views.realizar_servicio, name='realizar_servicio'),
    url(r'^$', views.inicio, name='servicios_realizados'),
    url(r'^tiposervicionuevo/$', views.tipo_servicio_ajax, name='nuevo_tipo_servicio'),
    url(r'^activacion/(?P<pk>[0-9]+)$', views.servicio_activacion, name='servicio_activacion'),
    url(r'^agregar_a_factura/(?P<pk>[0-9]+)/(?P<fact>[0-9]+)$', views.agregar_a_factura, name='agregar_a_factura'),
]
