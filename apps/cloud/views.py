import json
import requests

from apps.ajustes.models import Ajuste


def send_to_api(dictionary, model):
    # Obtener datos de la API
    ajuste = Ajuste.objects.only("api_url", "api_key").get(pk=1)

    # Obtener url y token
    api_url = ajuste.api_url + '/' + model
    api_token = ajuste.api_key

    # Diccionario a enviar
    params = json.dumps(dictionary).encode('utf8')

    # Headers para acceso a la Api
    headers = {'Authorization': 'Token token=' + api_token,
               'Content-Type': 'application/json'}

    response = requests.post(api_url, data=params, headers=headers)
    #print(str(response) + "- api_url: " + api_url + "- api_token: " + api_token)
