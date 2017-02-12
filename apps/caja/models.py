
from django.db import models
from django.utils import timezone

# Create your models here.
class Egresos(models.Model):
    """Registra la salida de dinero de caja"""
    cantidad = models.DecimalField(max_digits=5, decimal_places=2)
    concepto = models.CharField(max_length=200)
    usuario = models.ForeignKey('auth.User')
    fecha_egreso = models.DateTimeField(default=timezone.now)

class Caja(models.Model):
    """LLeva un resgistro del dinero en caja"""
    saldo = models.DecimalField(max_digits=6, decimal_places=2)
    usuario = models.ForeignKey('auth.User')
    fecha_apertura = models.DateTimeField(default=timezone.now)
    fecha_cierre = models.DateTimeField(null=True, blank=True)

class Capital(models.Model):
    """Registra el capital total"""
    monto = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
