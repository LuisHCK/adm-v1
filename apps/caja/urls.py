
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.inicio, name='caja_inicio'),
    url(r'^cierre/$', views.cierre_caja, name='cierre_caja'),
    url(r'^apertura/$', views.apertura_caja, name='apertura_caja')
]