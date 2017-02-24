
from django.db import models
from django.utils import timezone

# Create your models here.
class Articulos(models.Model):
    """Almacenar los detalles de los Articulos"""
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio_compra = models.DecimalField(max_digits=6, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=6, decimal_places=2)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    """Controlar la disponibilidad de los Articulos"""
    articulo = models.ForeignKey('Articulos', on_delete=models.CASCADE,)
    existencias = models.IntegerField()
    minimo_existencias = models.IntegerField(default=1)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    def __int__(self):
        return self.existencias
