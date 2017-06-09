
from django.db import models
from django.utils import timezone
# Create your models here.


class TypeService(models.Model):
    """Establece un tipo de servicio"""
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    code = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name

    def as_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            price=str(self.price),
            code=self.code)

class Service(models.Model):
    """Registra los servicios realizados"""
    user = models.ForeignKey('auth.User')
    description = models.TextField(max_length=150)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    type_service = models.ForeignKey(TypeService, null=True)
    quantity = models.IntegerField(default=1)
    invoice = models.ForeignKey('facturas.Invoice', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.description
