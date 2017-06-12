
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^nueva/$', views.MakeSale, name='MakeSale'),
    url(r'^$', views.Sales, name='sales'),
]