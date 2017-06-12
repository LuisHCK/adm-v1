
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Cash(models.Model):
    """LLeva un resgistro del dinero en cash"""
    balance = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ForeignKey('auth.User')
    opening_date = models.DateTimeField(null=True, blank=True)
    closing_date = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.balance)

class Money(models.Model):
    """Registra el capital total"""
    monto = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

# Create your models here.
class Expenses(models.Model):
    """Registra la salida de dinero de cash"""
    ESTADOS_EGRESO = (
        ('estado_pendiente', 'Pendiente'),
        ('estado_aprovado', 'Aprovado'),
        ('estado_denegado', 'Denegado'),
        )

    quantity = models.DecimalField(max_digits=7, decimal_places=2)
    details = models.CharField(max_length=200)
    user = models.ForeignKey('auth.User')
    status = models.CharField(max_length=50, choices=ESTADOS_EGRESO, default='estado_pendiente',
                              blank=True, null=True
                             )
    cash = models.ForeignKey(Cash, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(
        User, related_name='%(class)s_requests_created',
        on_delete=models.CASCADE, null=True, blank=True)
    charged = models.BooleanField(default=False)
    expense_date = models.DateTimeField(default=timezone.now)
