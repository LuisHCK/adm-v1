
from django.db import models
from django.utils import timezone
from apps.inventory.models import Product
from apps.services.models import TypeService

# Create your models here.


class Invoice(models.Model):
    '''Invoice una sale realizada a un client'''
    TIPOS = (
        ('contado', 'Contado'),
        ('credit', 'Credito'))
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'))

    user = models.ForeignKey('auth.User')
    client = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True)
    open = models.BooleanField(default=True)
    payment_type = models.CharField(max_length=15, choices=TIPOS, default='contado')
    status = models.CharField(max_length=15, choices=ESTADOS, default='pendiente')
    deadline = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    pay_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.client

    def product_count(self):
        '''Devolver la quantity de productos adquiridos'''
        product_items = InvoiceProducts.objects.filter(invoice=self).count()
        return product_items

    def service_count(self):
        '''Devuelve la quantity de serivicios adquiridos'''
        service_items = InvoiceServices.objects.filter(invoice=self).count()
        return service_items

    def clase(self):
        if self.status == 'pagado':
            return 'success'
        elif self.payment_type == 'credit' and timezone.now() < self.deadline:
            return 'warning'
        elif self.payment_type == 'credit' and timezone.now() > self.deadline:
            return 'danger'
        else:
            return 'faded'
    def _vencimiento(self):
        return self.deadline


class Abono(models.Model):
    '''Almacena los los abonos realizados a una invoice pendiente'''
    invoice = models.ForeignKey('invoices.Abono', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_abono = models.DateField(default=timezone.now)


#Creo que esta clase no se utiliza pero de da miedo borrarla
class InvoiceItems(models.Model):
    '''Almacena individualmente los items de una Invoice'''
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    details = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class InvoiceProducts(models.Model):
    '''Almacena el product que se planea vender'''
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class InvoiceServices(models.Model):
    '''Almacena el product que se planea vender'''
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    type_service = models.ForeignKey(TypeService, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
