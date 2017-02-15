
from django.db import models
from django.utils import timezone
from apps.inventario.models import Articulos

# Create your models here.

class Servicio(models.Model):
    """Registra los servicios realizados"""
    usuario = models.ForeignKey('auth.User')
    descripcion = models.TextField(max_length=150)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE, blank=True, null=True)
    articulos_cantidad = models.IntegerField(blank=True, null=True)
    fecha_servicio = models.DateTimeField(default=timezone.now)
