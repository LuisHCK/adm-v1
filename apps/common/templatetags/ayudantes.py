from django import template
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

register = template.Library()


@register.filter(name='avatar')
def avatar(user):
    avatar_perfil = user.perfil.foto.url
    return avatar_perfil


@register.filter(name='estado_solicitud_egreso')
def estado_solicitud_egreso(estado):
    if estado == 'estado_pendiente':
        return 'Pendiente'

    elif estado == 'estado_aprovado':
        return 'Aprovado'

    elif estado == 'estado_denegado':
        return 'Denegado'

    else:
        return 'Inválido'


@register.filter(name='estado_lista')
def estado_lista(estado):
    if estado == 'estado_pendiente':
        return None

    elif estado == 'estado_aprovado':
        return 'success'

    elif estado == 'estado_denegado':
        return 'warning'

    else:
        return 'danger'

@register.filter(name='servicio_subtotal')
def servicio_subtotal(item_servicio):
    return item_servicio.cantidad * item_servicio.tipo_servicio.costo

@register.filter(name='articulo_subtotal')
def articulo_subtotal(item_articulo):
    return item_articulo.cantidad * item_articulo.articulo.precio_venta
