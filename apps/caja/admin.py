
from django.contrib import admin
from .models import Cash, Money, Expenses

# Register your models here.
admin.site.register(Cash)
admin.site.register(Money)
admin.site.register(Expenses)
