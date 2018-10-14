
from django.db import models
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    """Almacenar los detalles de los Product"""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    purchase_price = models.DecimalField(max_digits=7, decimal_places=2)
    sale_price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    sale_price2 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    sale_price3 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    iva = models.DecimalField(max_digits=5, decimal_places=2)
    initial_ammount = models.DecimalField(max_digits=7, decimal_places=2)
    expires_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name

    def as_dict(self):
        '''Retorna un diccionario serializable'''
        return dict(
            id=str(self.id),
            name=self.name,
            code=self.code,
            sale_price=str(self.sale_price)
        )

class Inventory(models.Model):
    """Controlar la disponibilidad de los Product"""
    product = models.ForeignKey('Product', on_delete=models.CASCADE,)
    stocks = models.IntegerField()
    min_stocks = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    def __int__(self):
        return self.stocks

class Provider(models.Model):
    '''Proveedores de products'''
    VALORACIONES = (
        ('Excelente', 'excelente'),
        ('Muy bueno', 'muy_bueno'),
        ('Bueno', 'bueno'),
        ('Regular', 'regular'),
        ('Deficiente', 'deficiente'),
        ('Malo', 'malo'),
        ('Muy malo', 'muy_malo'),
        )

    '''Datos del provedor de products'''
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    description = models.TextField()
    direction = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    phone2 = models.CharField(max_length=30)
    assessment = models.CharField(max_length=50, choices=VALORACIONES,
                                  default='',
                                  blank=True, null=True)

