from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.Start, name='inicio_ajustes'),
    url(r'^guardar/$', views.guardar_ajustes, name='guardar_ajustes'),
    url(r'^cloud_guardar/$', views.guardar_cloud, name='guardar_ajustes_cloud'),
]
