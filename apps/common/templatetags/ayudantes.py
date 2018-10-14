from django import template
from django.contrib.auth.models import Group

from apps.settings.models import Settings

register = template.Library()


@register.filter(name='avatar')
def avatar(user):
    avatar_perfil = user.profile.picture.url
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
def servicio_subtotal(service_item):
    return service_item.quantity * service_item.type_service.price

@register.filter(name='articulo_subtotal')
def articulo_subtotal(product_item):
    return product_item.quantity * product_item.product.sale_price

@register.filter(name='ticket')
def ticket(var):
    '''Verifica que tipo de invoice se usa'''
    settings = Settings.objects.get(pk=1)
    if settings.tipo_factura == 'ticket':
        return True
    else:
        return False
