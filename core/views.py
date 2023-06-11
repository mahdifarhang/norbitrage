from django.shortcuts import render
from django.http.response import JsonResponse
from django.template.response import TemplateResponse
from core.tasks import load_market_orderbook, check_all_coins
from django.core.cache import cache


# Todo: Handle Permission
def market_list(request):
    market_list = [
        'USDTIRT',
        'BTCIRT',
        'BTCUSDT',
    ]
    return TemplateResponse(request=request, template="core/market_list.html", status=200,
                            context={'markets': market_list})


# Todo: Handle permissions
def load_orderbook(request, market):
    try:
        orderbook = load_market_orderbook(market)
        # print(cache.get('orderbook_data_IRTUSDT'))
        return JsonResponse({
            'status': 'OK',
            'result': orderbook,
        }, status=200)
    except Exception as exp:
        return JsonResponse({
            'status': 'Not OK',
            'error': f'Error Happened: {exp}'
        }, status=400)

def check_coin_price_difference(request):
    try:
        check_all_coins.delay()
        return JsonResponse({
            'status': 'OK',
        }, status=200)
    except Exception as exp:
        return JsonResponse({
            'status': 'Not OK',
            'error': f'Error Happened: {exp}'
        }, status=400)
