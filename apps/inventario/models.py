
from django.db import models
from django.utils import timezone

# Create your models here.
class Articulos(models.Model):
    """Almacenar los detalles de los Articulos"""
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True)
    precio_compra = models.DecimalField(max_digits=7, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=7, decimal_places=2)
    precio_venta2 = models.DecimalField(max_digits=7, decimal_places=2)
    precio_venta3 = models.DecimalField(max_digits=7, decimal_places=2)
    iva = models.DecimalField(max_digits=5, decimal_places=2)
    cantidad_inicial = models.DecimalField(max_digits=7, decimal_places=2)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    """Controlar la disponibilidad de los Articulos"""
    articulo = models.ForeignKey('Articulos', on_delete=models.CASCADE,)
    existencias = models.IntegerField()
    minimo_existencias = models.IntegerField(default=1)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    def __int__(self):
        return self.existencias

class Proveedor(models.Model):
    '''Proveedores de articulos'''
    VALORACIONES = (
        ('Excelente', 'excelente'),
        ('Muy bueno', 'muy_bueno'),
        ('Bueno', 'bueno'),
        ('Regular', 'regular'),
        ('Deficiente', 'deficiente'),
        ('Malo', 'malo'),
        ('Muy malo', 'muy_malo'),
        )

    '''Datos del provedor de articulos'''
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20)
    descripcion = models.TextField()
    direccion = models.TextField()
    email = models.EmailField()
    telefono = models.CharField(max_length=30)
    telefono2 = models.CharField(max_length=30)
    valoracion = models.CharField(max_length=50, choices=VALORACIONES,
                                  default='',
                                  blank=True, null=True)

