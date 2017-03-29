from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ver_perfiles, name='perfiles'),
    url(r'^(?P<pk>[0-9]+)/$', views.ver_perfil, name='ver_perfil'),
    url(r'^(?P<pk>[0-9]+)/editar/$', views.editar_perfil, name='editar_perfil'),
]
