
def es_administrador(user):
    '''Verificar que el usuario es Administrador'''
    if user.groups.filter(name__in=['Administrador']) or user.is_staff:
        return True
    else:
        return False


def es_cajero(user):
    '''Verificar que el usuario es Cajero'''
    if user.groups.filter(name__in=['Cajero']):
        return True
    else:
        return False
