def es_administrador(user):
    if user.groups.filter(name__in=['Administrador']):
        return True
    else:
        return False