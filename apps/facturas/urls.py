
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.facturas, name='facturas'),
    url(r'^nuevo/$', views.nueva_factura, name='nueva_factura'),
    url(r'^(?P<pk>[0-9]+)/eliminar/$', views.eliminar_factura, name='eliminar_factura'),
    #url(r'^(?P<pk>[0-9]+)/items/$', views.eliminar_item, name='eliminar_item'),

    # Items para la factura
    url(r'^(?P<pk>[0-9]+)/articulos/$', views.agregar_articulo, name='agregar_articulo_factura'),
    url(r'^articulos/(?P<articulo>[0-9]+)/eliminar/$',
        views.eliminar_articulos, name='eliminar_articulos_factura'),

    url(r'^(?P<pk>[0-9]+)/servicios/$', views.agregar_servicio, name='agregar_servicio_factura'),
    url(r'^servicios/(?P<servicio>[0-9]+)/eliminar/$',
        views.eliminar_servicios, name='eliminar_servicios_factura'),

    ##
    url(r'^(?P<pk>[0-9]+)/$', views.detalles_factura, name='detalles_factura'),
    url(r'^pagadas/$', views.facturas_pagadas, name='facturas_pagadas'),
    url(r'^pendientes/$', views.facturas_pendientes, name='facturas_pendientes'),
    url(r'^cobrar/(?P<pk>[0-9]+)$', views.cobrar_factura, name='cobrar_factura'),
]