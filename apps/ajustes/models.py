from django.db import models

class Ajuste(models.Model):
    '''Guarda los ajustes del sistema'''
    # Datos de la empresa
    nombre = models.CharField(max_length=25)
    direccion = models.TextField(max_length=100)
    telefono = models.CharField(max_length=25)
    email = models.EmailField(null=True, blank=True)
    # Datos de ventas
    simbolo_moneda = models.CharField(max_length=10, default='C$')
    ruc = models.CharField(max_length=100, null=True, blank=True)
    