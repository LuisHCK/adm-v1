
from django.db import models
from django.utils import timezone

# Create your models here.


class Factura(models.Model):
    """Factura una venta realizada a un cliente"""
    usuario = models.ForeignKey('auth.User')
    cliente = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True)
    cobrada = models.BooleanField(default=False)
    fecha_factura = models.DateField(default=timezone.now)

    def cobrar(self):
        """Si la factura es pagada se guarda"""
        self.cobrada = True
        self.save()

    def __str__(self):
        return self.cliente


class FacturaItems(models.Model):
    """Almacena individualmente los items de una Factura"""
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    concepto = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
