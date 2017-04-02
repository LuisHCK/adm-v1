from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Perfil

class PerfilInLine(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'
    fk_name = 'usuario'

class CustomUsuarioAdmin(UserAdmin):
    inlines = (PerfilInLine, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUsuarioAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUsuarioAdmin)
