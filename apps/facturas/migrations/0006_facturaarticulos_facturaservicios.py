# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_auto_20170208_0521'),
        ('servicios', '0005_auto_20170216_1812'),
        ('facturas', '0005_auto_20170214_1726'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacturaArticulos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('articulo', models.ForeignKey(to='inventario.Articulos')),
            ],
        ),
        migrations.CreateModel(
            name='FacturaServicios',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('servicio', models.ForeignKey(to='servicios.Servicio')),
            ],
        ),
    ]
