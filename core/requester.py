from django.conf import settings


class Requester():
    base_url = getattr(settings, 'NOBITEX_API_BASE_URL', 'https://api.nobitex.ir/')
    endpoint = None

