
from django.contrib import admin
from .models import Articulos
from .models import Inventario

# Register your models here.
admin.site.register(Articulos)
admin.site.register(Inventario)
