
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.AllInvoices, name='AllInvoices'),
    url(r'^nuevo/$', views.NewInvoice, name='NewInvoice'),
    url(r'^(?P<pk>[0-9]+)/eliminar/$', views.DeleteInvoice, name='DeleteInvoice'),
    #url(r'^(?P<pk>[0-9]+)/items/$', views.eliminar_item, name='eliminar_item'),

    # Items para la invoice
    url(r'^(?P<pk>[0-9]+)/products/$', views.AddProduct, name='agregar_articulo_factura'),
    url(r'^products/(?P<product>[0-9]+)/eliminar/$',
        views.DeleteProduct, name='eliminar_articulos_factura'),

    url(r'^(?P<pk>[0-9]+)/services/$', views.AddService, name='agregar_servicio_factura'),
    url(r'^services/(?P<service>[0-9]+)/eliminar/$',
        views.DeleteService, name='eliminar_servicios_factura'),

    ##
    url(r'^(?P<pk>[0-9]+)/$', views.InvoiceDetails, name='InvoiceDetails'),
    url(r'^cobrar/(?P<pk>[0-9]+)$', views.BillInvoice, name='BillInvoice'),
    url(r'^SearchProduct/(?P<code>[\w\-]+)/$', views.SearchProduct, name="SearchProduct"),
    url(r'^SearchService/(?P<code>[\w\-]+)/$', views.SearchService, name="SearchService"),
]