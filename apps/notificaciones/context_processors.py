
from apps.cash.models import Cash
from apps.notificaciones.models import Notificacion


def lista_notificaciones(request):
    mensajes_caja = {}
    total_notif = 0
    if Cash.objects.filter(closing_date=None).count() == 0:
        mensajes_caja['tipo'] = 'error'
        mensajes_caja['texto'] = "Aún no se ha realizado la apertura de cash."
        total_notif += 1

    # Notificaciones de invoices

    notif = Notificacion.objects.all()
    total_notif += notif.count()
    return{
        'notificaciones': notif,
        'mensajes_caja': mensajes_caja,
        'total_notif': total_notif,
    }
