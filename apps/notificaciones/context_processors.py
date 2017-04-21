
from apps.caja.models import Caja
from apps.notificaciones.models import Notificacion


def lista_notificaciones(request):
    mensajes_caja = {}
    total_notif = 0
    if Caja.objects.filter(fecha_cierre=None).count() == 0:
        mensajes_caja['tipo'] = 'error'
        mensajes_caja['texto'] = "Aún no se ha realizado la apertura de caja."
        total_notif += 1

    notif = Notificacion.objects.all()
    total_notif += notif.count()
    return{
        'notificaciones': notif,
        'mensajes_caja': mensajes_caja,
        'total_notif': total_notif,
    }
