# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 18:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0004_auto_20170216_1744'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servicio',
            old_name='articulos_cantidad',
            new_name='cantidad',
        ),
        migrations.RemoveField(
            model_name='servicio',
            name='articulo',
        ),
    ]