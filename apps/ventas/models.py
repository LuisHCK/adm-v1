
from django.db import models
from django.utils import timezone
from apps.inventario.models import Articulos
from apps.facturas.models import Factura

# Create your models here.

class Venta(models.Model):
    """Realiza la venta de un producto"""
    usuario = models.ForeignKey('auth.User')
    articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    total = models.DecimalField(max_digits=6, decimal_places=2)
    descuento = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, null=True, blank=True)
    fecha_venta = models.DateTimeField(default=timezone.now)
