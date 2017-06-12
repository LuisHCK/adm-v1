
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^nueva/$', views.realizar_venta, name='realizar_venta'),
    url(r'^$', views.Sales, name='ventas'),
]