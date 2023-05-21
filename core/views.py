from django.shortcuts import render
from django.http.response import JsonResponse
from django.conf import settings
# Create your views here.

def test_view(request):
    return JsonResponse({
        'pong': True,
        'status': 'OK',
    }, status=200)


def get_orders(request):
    base_url = getattr(settings, 'NOBITEX_API_BASE_URL', 'https://api.nobitex.ir/')