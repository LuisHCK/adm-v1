from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    """Contiene los datos personales de los usuarios"""
    user = models.OneToOneField('auth.User')
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    identification_card = models.CharField(max_length=200)
    direction = models.TextField(max_length=200)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    birthdate = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    depurate_date = models.DateField(blank=True, null=True)
    picture = models.ImageField(upload_to='media/', default='img/avatar.png', blank=True, null=True)
    def __str__(self):
        return self.name+" "+self.last_name


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
