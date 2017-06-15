
from django.conf.urls import include, url
from . import views

urlpatterns = [
    #url(r'^$', views.Start, name='Start'),
    url(r'^$', views.InventoryList, name='ShowInventory'),
    url(r'^product/(?P<pk>[0-9]+)/$', views.ProductDetails, name='ShowProduct'),
    url(r'^actualizar/(?P<pk>[0-9]+)/$', views.UpdateStock, name='UpdateStock'),
    url(r'^product/nuevo', views.NewProduct, name='NewProduct'),
    url(r'^product/ajax', views.NewProductAjax, name='NewProductAjax'),
    url(r'^eliminar/(?P<pk>[0-9]+)/$', views.DeleteProductAjax, name='DeleteProductAjax')
]