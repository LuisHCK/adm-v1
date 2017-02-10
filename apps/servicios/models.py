from django.db import models
from django.utils import timezone

# Create your models here.

class Servicio(models.Model):
    """Registra los servicios realizados"""
    usuario = models.ForeignKey('auth.User')
    descripcion = models.TextField(max_length=200)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    fecha_servicio = models.DateTimeField(default=timezone.now)
