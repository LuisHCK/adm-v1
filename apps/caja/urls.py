
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.inicio, name='caja_inicio'),
    url(r'^cierre/$', views.cierre_caja, name='cierre_caja'),
    url(r'^primera_apertura/$', views.primera_apertura, name='primera_apertura'),
    url(r'^apertura_ajax/(?P<pk>[0-9]+)/$', views.apertura_ajax, name='apertura_ajax'),
    url(r'^capital/$', views.estado_capital, name='estado_capital'),
    url(r'^egresos/(?P<pk>[0-9]+)/$', views.detalles_egreso, name='detalles_egreso'),
    url(r'^egresos/nuevo/', views.egreso_caja, name='nuevo_egreso'),
    url(r'^egresos/$', views.ver_egresos, name='ver_egresos'),
    url(r'^egresos/(?P<pk>[0-9]+)/(?P<accion>[\w\-]+)/$', views.aprovar_egreso,
        name='aprovar_egreso'),
    url(r'^egresos/cobrar/(?P<pk>[0-9]+)/$', views.cobrar_egreso, name='cobrar_egreso'),
]