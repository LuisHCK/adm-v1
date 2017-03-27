from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Perfil(models.Model):
    """Contiene los datos personales de los usuarios"""
    usuario = models.OneToOneField('auth.User')
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    cedula = models.CharField(max_length=200)
    direccion = models.TextField(max_length=200)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(blank=False, null=False)
    fecha_entrada = models.DateField(blank=False, null=False)
    fecha_salida = models.DateField(blank=True, null=True)
    foto = models.ImageField(upload_to='media/', default='img/avatar.png')

    def __str__(self):
        return self.nombres+" "+self.apellidos

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
    instance.perfil.save()
