import json

from core.requester import APIRequester
from django.core.cache import cache


def load_market_orderbook(market:str):
    requester = APIRequester()
    # Todo: Handle wrong market input (Problem1: doesn't exist)
    endpoint = f'/v2/orderbook/{market}'
    response = requester(endpoint)
    cache.set(f'orderbook_data_UDSTIRT_USDTIRT', response, 60)
    return response
