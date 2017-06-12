from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ShowProfiles, name='profiles'),
    url(r'^(?P<pk>[0-9]+)/$', views.ShowProfile, name='ShowProfile'),
    url(r'^(?P<pk>[0-9]+)/editar/$', views.EditProfiles, name='EditProfiles'),
]
