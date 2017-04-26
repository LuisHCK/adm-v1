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
