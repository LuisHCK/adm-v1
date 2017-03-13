from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

''' Este modelo crea una instancia de uno a uno con la tabla auth.user, con el proposito
de agregar nuevos campos y mantener el buen sistema de autenticacion de django.
'''

class Perfil(models.Model):
	usuario = models.OneToOneField(User, on_delete=models.CASCADE)
	cedula = models.CharField(null=False, default="000-000000-00000", max_length=16)
	telefono = models.CharField(max_length=16, default="+000-0000-0000")
	puesto = models.CharField(max_length=50, default="Empleado")
	direccion = models.CharField(max_length=150, default="-")
	foto = models.ImageField(upload_to='media/', default='media/user.png')

	@classmethod
	def create(cls, usuario_p):
		perfil = cls(usuario=usuario_p)
		return perfil

	''' Los siguientes dos metodos se entrelazan con el modelo de usuarios de django
	cuando se lanza un evento de guardado.
	
	@receiver(post_save, sender=User)
	def crear_usuario(sender, instance, created, **kwargs):
		if created:
			Perfil.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def guardar_usuario(selder, instance, **kwargs):
		instance.Perfil.save()
'''


