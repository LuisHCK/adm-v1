
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^nuevo/$', views.PerformService, name='PerformService'),
    url(r'^$', views.Start, name='servicios_realizados'),
    url(r'^tiposervicionuevo/$', views.TypeServiceAjax, name='nuevo_tipo_servicio'),
    url(r'^activacion/(?P<pk>[0-9]+)$', views.ActivateService, name='ActivateService'),
    url(r'^AddToInvoice/(?P<pk>[0-9]+)/(?P<fact>[0-9]+)$', views.AddToInvoice, name='AddToInvoice'),
    url(r'^FastService/$', views.ServiceAjax, name='ServiceAjax'),
]
