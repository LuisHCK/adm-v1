
from django.db import models
from django.utils import timezone
from apps.inventario.models import Product
from apps.facturas.models import Invoice

# Create your models here.

class Sale(models.Model):
    """Realiza la venta de un producto"""
    user = models.ForeignKey('auth.User')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
