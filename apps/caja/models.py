
from django.db import models
from django.utils import timezone
from apps.ventas.models import Venta

# Create your models here.
class Factura(models.Model):
    """Guarda un registro de la transaccion realizada"""
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, blank=True)
    cantidad = models.DecimalField(max_digits=6, decimal_places=2)
    concepto = models.CharField(max_length=200)
    usuario = models.ForeignKey('auth.User')
    fecha_entrada = models.DateTimeField(timezone.now)

class Egresos(models.Model):
    """Registra la salida de dinero de caja"""
    cantidad = models.DecimalField(max_digits=5, decimal_places=2)
    concepto = models.CharField(max_length=200)
    usuario = models.ForeignKey('auth.User')
    fecha_egreso = models.DateTimeField(timezone.now)

class Caja(models.Model):
    """LLeva un resgistro del dinero en caja"""
    saldo = models.DecimalField(max_digits=6, decimal_places=2)
    usuario = models.ForeignKey('auth.User')
    fecha_entrada = models.DateTimeField(timezone.now)
    fecha_cierre = models.DateTimeField(blank=True)
