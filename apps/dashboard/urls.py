
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.Start, name='Start'),
    url(r'^venta_rapida/$', views.SaleAjax, name='SaleAjax'),
    url(r'^servicio_rapido/$', views.ServiceAjax, name='ServiceAjax'),
]
