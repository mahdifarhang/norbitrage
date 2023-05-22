from django.shortcuts import render
from django.http.response import JsonResponse
from core.tasks import load_market_orderbook

# Todo: Handle permissions
def load_orderbook(request, market):
    try:
        orderbook = load_market_orderbook(market)
        return JsonResponse({
            'status': 'OK',
            'result': orderbook,
        }, status=200)
    except Exception as exp:
        return JsonResponse({
            'status': 'Not OK',
            'error': f'Error Happened: {exp}'
        }, status=400)