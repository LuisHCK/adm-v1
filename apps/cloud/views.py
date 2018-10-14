import json
import threading

import requests

from apps.settings.models import Settings
from apps.cash.models import Cash


def send_to_api(dictionary, model):
    try:
        # Obtener datos de la API
        ajuste = Settings.objects.only("api_url", "api_key").get(pk=1)

        # Obtener url y token
        api_url = ajuste.api_url + '/' + model
        api_token = ajuste.api_key

        # Diccionario a enviar
        params = json.dumps(dictionary).encode('utf8')

        # Headers para acceso a la Api
        headers = {'Authorization': 'Token token=' + api_token,
                   'Content-Type': 'application/json'}

        send_task = threading.Thread(target=sender, args=(
            api_url, api_token, params, headers))
        send_task.setDaemon(False)
        send_task.start()

    except:
        print("<------ Failed to send data to server ------>")


def sender(api_url, api_token, params, headers):
    response = requests.post(api_url, data=params, headers=headers)
    print(str(response.status_code) + "- api_url: " +
          api_url + "- api_token: " + api_token)
