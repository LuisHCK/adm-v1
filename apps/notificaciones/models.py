from django.db import models
from django.utils import timezone

class Notificacion(models.Model):
    '''Almacena notificaciones del sistema'''
    tipo = models.TextField(max_length=25)
    texto = models.TextField(max_length=300)
    status = models.BooleanField(default=False)
    deadline = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    

