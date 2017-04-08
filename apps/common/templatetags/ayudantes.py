from django import template
from django.contrib.auth.models import Group 
from django.shortcuts import get_object_or_404

register = template.Library() 

@register.filter(name='avatar')
def avatar(user):
    avatar_perfil = user.perfil.foto.url
    return avatar_perfil