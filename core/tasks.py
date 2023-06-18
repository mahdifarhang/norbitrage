from django.conf import settings
from decimal import Decimal
from celery import shared_task

from core.requester import APIRequester
from django.core.cache import cache

coin_list = [
    'BTC',
    'ETH',
    'DOGE',
    'SHIB',
    '100K_FLOKI',
    'XRP',
    'FTM',
    'MATIC',
    'BNB',
    'TRX',
]
def load_market_orderbook(market:str):
    requester = APIRequester()
    # Todo: Handle wrong market input (Problem1: doesn't exist)
    endpoint = f'/v2/orderbook/{market}'
    response = requester(endpoint)
    cache.set(f'orderbook_data_UDSTIRT_USDTIRT', response, 60)
    check_coin('BTC')
    return response


def check_coin(coin):
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
        text = f"___________{coin}___________\n" \
               f"profits: USDT -> IRT\n" \
               f"Buy Price: {buy_in_usdt_sell_in_irt['buy_price']}\n" \
               f"Sell Price: {buy_in_usdt_sell_in_irt['sell_price']}\n"
        print(text)
        send_telegram.delay(text)

    if buy_in_irt_sell_in_usdt['buy_price'] < buy_in_irt_sell_in_usdt['sell_price']:
        text = f"___________{coin}___________\n" \
               f"profits: IRT -> USDT\n" \
               f"Buy Price: {buy_in_irt_sell_in_usdt['buy_price']}\n" \
               f"Sell Price: {buy_in_irt_sell_in_usdt['sell_price']}\n"
        print(text)
        send_telegram.delay(text)
@shared_task(name='check_all_coins')
def check_all_coins(coins=coin_list):
    for coin in coins:
        check_coin(coin)

@shared_task()
def send_telegram(message):
    telegram_bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', 'hellow-world')
    telegram_chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', 'hellow-world')
    requester = APIRequester('https://api.telegram.org')
    usdt_response = requester(f'/bot{telegram_bot_token}/sendMessage', data={
        'chat_id': telegram_chat_id,
        'text': message
    })