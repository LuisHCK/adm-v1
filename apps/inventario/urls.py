
from django.conf.urls import include, url
from . import views

urlpatterns = [
    #url(r'^$', views.inicio, name='inicio'),
    url(r'^$', views.InventoryList, name='ver_inventario'),
    url(r'^product/(?P<pk>[0-9]+)/$', views.ProductDetails, name='ver_articulo'),
    url(r'^actualizar/(?P<pk>[0-9]+)/$', views.UpdateStock, name='act_existencias'),
    url(r'^product/nuevo', views.NewProduct, name='crear_articulo'),
    url(r'^product/ajax', views.NewProductAjax, name='ajax_crear_articulo'),
    url(r'^eliminar/(?P<pk>[0-9]+)/$', views.DeleteProductAjax, name='eliminar_articulo')
]