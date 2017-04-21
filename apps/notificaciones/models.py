from django.db import models
from django.utils import timezone

class Notificacion(models.Model):
    '''Almacena notificaciones del sistema'''
    tipo = models.TextField(max_length=25)
    texto = models.TextField(max_length=300)
    estado = models.BooleanField(default=False)
    fecha_limite = models.DateTimeField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    

