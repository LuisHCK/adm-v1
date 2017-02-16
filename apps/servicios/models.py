
from django.db import models
from django.utils import timezone

# Create your models here.


class TipoServicio(models.Model):
    """Establece un tipo de servicio"""
    nombre = models.CharField(max_length=150)
    costo = models.DecimalField(max_digits=6, decimal_places=2)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    """Registra los servicios realizados"""
    usuario = models.ForeignKey('auth.User')
    descripcion = models.TextField(max_length=150)
    precio = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tipo_servicio = models.ForeignKey(TipoServicio, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    fecha_servicio = models.DateTimeField(default=timezone.now)
