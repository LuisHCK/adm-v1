
from django.conf.urls import include, url
from . import views

urlpatterns = [
    #url(r'^$', views.inicio, name='inicio'),
    url(r'^$', views.lista_inventario, name='ver_inventario'),
    url(r'^articulo/(?P<pk>[0-9]+)/$', views.detalles_articulo, name='ver_articulo'),
    url(r'^existencias/(?P<pk>[0-9]+)/editar/$', views.actualizar_existencias,
        name='act_existencias'),
    url(r'^articulo/nuevo', views.nuevo_articulo, name='crear_articulo'),
    url(r'^articulo/ajax', views.nuevo_articulo_ajax, name='ajax_crear_articulo'),
    url(r'^eliminar/(?P<pk>[0-9]+)/$', views.eliminar_articulo_ajax, name='eliminar_articulo')
]