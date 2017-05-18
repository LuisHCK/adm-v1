import json
import urllib

from apps.ajustes.models import Ajuste

def send_to_api(dictionary, user_id, model):
    ajuste = Ajuste.objects.only("api_url", "api_key").get(pk=user_id)
    api_url = ajuste.api_url+model
    api_token = ajuste.api_key

    params = json.dumps(dictionary).encode('utf8')
    request = urllib.request.Request(api_url, data=params,
                                     headers={'Authorization':'Token token='+api_token,
                                              'Content-Type':'application/json'})
    response = urllib.request.urlopen(request)
    print(response.read().decode('utf8'))
