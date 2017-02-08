
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.inicio, name='inicio'),
]