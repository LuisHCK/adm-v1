
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.Start, name='caja_inicio'),
    url(r'^cierre/$', views.CloseCash, name='CloseCash'),
    url(r'^FirstCash/$', views.FirstCash, name='FirstCash'),
    url(r'^OpenCashAjax/(?P<pk>[0-9]+)/$', views.OpenCashAjax, name='OpenCashAjax'),
    url(r'^capital/$', views.MoneyState, name='MoneyState'),
    url(r'^egresos/(?P<pk>[0-9]+)/$', views.detalles_egreso, name='detalles_egreso'),
    url(r'^egresos/nuevo/', views.RequestExpense, name='nuevo_egreso'),
    url(r'^egresos/$', views.ShowExpenses, name='ShowExpenses'),
    url(r'^egresos/(?P<pk>[0-9]+)/(?P<accion>[\w\-]+)/$', views.ApproveExpense,
        name='ApproveExpense'),
    url(r'^egresos/cobrar/(?P<pk>[0-9]+)/$', views.ChargeExpenses, name='ChargeExpenses'),
]