
from django.db import models
from django.utils import timezone
from apps.inventario.models import Articulos
from apps.servicios.models import TipoServicio

# Create your models here.


class Factura(models.Model):
    '''Factura una venta realizada a un cliente'''
    usuario = models.ForeignKey('auth.User')
    cliente = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True)
    cerrada = models.BooleanField(default=False) # La factura un está siendo creada
    contado = models.BooleanField(default=True) # La factura es al crédito o de contado
    pagada = models.BooleanField(default=False) # la factura al crédito fue pagada por el cliente
    fecha_limite = models.DateTimeField(blank=True, null=True)
    fecha_factura = models.DateTimeField(default=timezone.now)
    fecha_cobro = models.DateTimeField(blank=True, null=True)

    def cobrar(self):
        '''Si la factura es pagada se guarda'''
        self.cerrada = True
        self.fecha_cobro = timezone.now()
        self.save()

    def __str__(self):
        return self.cliente

    def productos_count(self):
        '''Devolver la cantidad de productos adquiridos'''
        item_articulos = FacturaArticulos.objects.filter(factura=self).count()
        return item_articulos

    def servicios_count(self):
        '''Devuelve la cantidad de serivicios adquiridos'''
        item_servicios = FacturaServicios.objects.filter(factura=self).count()
        return item_servicios

    def estado(self):
        '''Devuelve el estado en que se encuentra una factura'''
        estado = object
        if self.contado:
            estado = {'class': 'success', 'mensaje': 'Factura de Contado'}

        elif self.pagada is True:
            estado = {'class': 'success', 'mensaje': 'Factura pagada'}

        elif self.contado is False and timezone.now() < self.fecha_limite:
            estado = {'class': 'warning', 'mensaje': 'Factura de pendiente de cobro'}

        elif self.contado is False and timezone.now() >= self.fecha_limite:
            estado = {'class': 'danger', 'mensaje': 'Se venció la fecha limite de pago'}

        else:
            estado = {'class': 'warning', 'mensaje': 'La factura no es válida'}

        return estado

class FacturaItems(models.Model):
    '''Almacena individualmente los items de una Factura'''
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    concepto = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2)


class FacturaArticulos(models.Model):
    '''Almacena el articulo que se planea vender'''
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)


class FacturaServicios(models.Model):
    '''Almacena el articulo que se planea vender'''
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    tipo_servicio = models.ForeignKey(TipoServicio, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
