"""administra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from apps.usuarios import views as user_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'', include('apps.dashboard.urls')),
    url(r'^login/$', user_views.iniciar_sesion, name='login'),
    url(r'^logout/$', user_views.cerrar_sesion, name='logout'),
    url(r'^signup/$', user_views.crear_cuenta, name='signup'),
    url(r'^configuracion/$', user_views.configuracion, name='configuracion'),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', admin.site.urls),
    url(r'^inventario/', include('apps.inventario.urls')),
    url(r'^ventas/', include('apps.ventas.urls')),
    url(r'^caja/', include('apps.caja.urls')),
    url(r'^servicios/', include('apps.servicios.urls')),
    url(r'^facturas/', include('apps.facturas.urls')),
    url(r'^usuarios/', include('apps.usuarios.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
