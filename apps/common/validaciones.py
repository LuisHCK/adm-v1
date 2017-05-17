def es_administrador(user):
    if user.groups.filter(name__in=['Administrador']) or user.is_staff:
        return True
    else:
        return False

def es_cajero(user):
    if user.groups.filter(name__in=['Cajero']):
        return True
    else:
        return False
