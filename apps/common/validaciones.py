def es_administrador(user):
    if user.groups.filter(name__in=['Administrador']):
        return True
    else:
        return False

def es_cajero(user):
    if user.groups.filter(name__in=['Cajero']):
        return True
    else:
        return False
