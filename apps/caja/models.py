
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Caja(models.Model):
    """LLeva un resgistro del dinero en caja"""
    saldo = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ForeignKey('auth.User')
    fecha_apertura = models.DateTimeField(null=True, blank=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.saldo)

class Capital(models.Model):
    """Registra el capital total"""
    monto = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

# Create your models here.
class Egresos(models.Model):
    """Registra la salida de dinero de caja"""
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
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE)
    aprovado_por = models.ForeignKey(
        User, related_name='%(class)s_requests_created',
        on_delete=models.CASCADE, null=True, blank=True)
    cobrado = models.BooleanField(default=False)
    fecha_egreso = models.DateTimeField(default=timezone.now)
