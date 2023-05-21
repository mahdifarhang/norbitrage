import urllib

from django.conf import settings

nobitex_token = getattr(settings, 'NOBITEX_AUTHORIZATION_TOKEN', 'default_token')

import requests

url = "https://api.nobitex.ir/v2/orderbook/BTCUSDT"

payload={}
headers = {
  'Authorization': f'Token { nobitex_token }'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
