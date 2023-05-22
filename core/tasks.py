import json

from core.requester import APIRequester



def load_market_orderbook(market:str):
    requester = APIRequester()
    # Todo: Handle wrong market input
    endpoint = f'/v2/orderbook/{market}'
    response = requester(endpoint)
    return response
