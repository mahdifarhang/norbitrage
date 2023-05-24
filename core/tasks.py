import json
from decimal import Decimal

from core.requester import APIRequester
from django.core.cache import cache


def load_market_orderbook(market:str):
    requester = APIRequester()
    # Todo: Handle wrong market input (Problem1: doesn't exist)
    endpoint = f'/v2/orderbook/{market}'
    response = requester(endpoint)
    cache.set(f'orderbook_data_UDSTIRT_USDTIRT', response, 60)
    check_coin('BTC')
    return response


def check_coin(coin='BTC'):
    requester = APIRequester()
    usdt_response = requester(f'v2/orderbook/{coin}USDT')
    irt_response = requester(f'v2/orderbook/{coin}IRT')
    usdt_irt_response = requester('v2/orderbook/USDTIRT')
    usdt_bids = usdt_response.get('bids')
    irt_bids = irt_response.get('bids')
    usdt_asks = usdt_response.get('asks')
    irt_asks = irt_response.get('asks')
    buy_in_usdt_sell_in_irt = {
        'buy_price': Decimal(usdt_bids[0][0]),
        'sell_price': Decimal(irt_asks[0][0]) / Decimal(usdt_irt_response.get('lastTradePrice')),
    }
    buy_in_irt_sell_in_usdt = {
        'buy_price': Decimal(irt_bids[0][0]),
        'sell_price': Decimal(usdt_asks[0][0]) * Decimal(usdt_irt_response.get('lastTradePrice')),
    }

    if buy_in_usdt_sell_in_irt['buy_price'] < buy_in_usdt_sell_in_irt['sell_price']:
        print('____________________')
        print('profits: USDT -> IRT')
        print(f"Buy Price: {buy_in_usdt_sell_in_irt['buy_price']}")
        print(f"Sell Price: {buy_in_usdt_sell_in_irt['sell_price']}")

    if buy_in_irt_sell_in_usdt['buy_price'] < buy_in_irt_sell_in_usdt['sell_price']:
        print('____________________')
        print('profits: IRT -> USDT')
        print(f"Buy Price: {buy_in_irt_sell_in_usdt['buy_price']}")
        print(f"Sell Price: {buy_in_irt_sell_in_usdt['sell_price']}")
