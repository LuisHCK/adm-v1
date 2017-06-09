from django import template
from django.contrib.auth.models import Group

from apps.ajustes.models import Ajuste

register = template.Library()


@register.filter(name='avatar')
def avatar(user):
    avatar_perfil = user.perfil.foto.url
    return avatar_perfil


@register.filter(name='estado_solicitud_egreso')
def estado_solicitud_egreso(status):
    if status == 'estado_pendiente':
        return 'Pendiente'

    elif status == 'estado_aprovado':
        return 'Aprovado'

    elif status == 'estado_denegado':
        return 'Denegado'

    else:
        return 'Inválido'


@register.filter(name='estado_lista')
def estado_lista(status):
    if status == 'estado_pendiente':
        return None

    elif status == 'estado_aprovado':
        return 'success'

    elif status == 'estado_denegado':
        return 'warning'

    else:
        return 'danger'

@register.filter(name='servicio_subtotal')
def servicio_subtotal(item_servicio):
    return item_servicio.quantity * item_servicio.type_service.price

@register.filter(name='articulo_subtotal')
def articulo_subtotal(item_articulo):
    return item_articulo.quantity * item_articulo.product.sale_price

@register.filter(name='ticket')
def ticket(var):
    '''Verifica que tipo de invoice se usa'''
    ajustes = Ajuste.objects.get(pk=1)
    if ajustes.tipo_factura == 'ticket':
        return True
    else:
        return False
