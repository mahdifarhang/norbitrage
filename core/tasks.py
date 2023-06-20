from django.conf import settings
from decimal import Decimal
from celery import shared_task

from core.requester import APIRequester
from core.telegram import send_telegram_message
from django.core.cache import cache

COIN_LIST = [
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

def get_USDTIRT_price():
    price = cache.get('USDTIRT_price')
    if price:
        return price
    return update_USDTIRT_cache_price()

@shared_task(name='update_USDTIRT_cache_price')
def update_USDTIRT_cache_price():
    requester = APIRequester()
    response = requester('v2/orderbook/USDTIRT')
    price = response.get('lastTradePrice')
    if price:
        cache.set(f'USDTIRT_price', price)
        return price
    return None

def load_market_orderbook(market:str):
    requester = APIRequester()
    # Todo: Handle wrong market input (Problem1: doesn't exist)
    endpoint = f'/v2/orderbook/{market}'
    response = requester(endpoint)
    cache.set(f'orderbook_data_UDSTIRT_USDTIRT', response, 60)
    return response

def check_coin(coin):
    requester = APIRequester()
    usdt_response = requester(f'v2/orderbook/{coin}USDT')
    irt_response = requester(f'v2/orderbook/{coin}IRT')
    usdtirt_price = get_USDTIRT_price() or '0'
    usdt_bids = usdt_response.get('bids')
    usdt_asks = usdt_response.get('asks')

    irt_bids = irt_response.get('bids')
    irt_asks = irt_response.get('asks')

    buy_in_usdt_sell_in_irt = {
        'buy_price': Decimal(usdt_bids[0][0]),
        'sell_price': Decimal(irt_asks[0][0]) / Decimal(usdtirt_price),
        'amount': min(Decimal(usdt_bids[0][1]), Decimal(irt_asks[0][1])),
    }
    buy_in_irt_sell_in_usdt = {
        'buy_price': Decimal(irt_bids[0][0]),
        'sell_price': Decimal(usdt_asks[0][0]) * Decimal(usdtirt_price),
        'amount': min(Decimal(irt_bids[0][1]), Decimal(usdt_asks[0][1])),
    }

    text = ''
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID')
    if buy_in_usdt_sell_in_irt['buy_price'] < buy_in_usdt_sell_in_irt['sell_price']:
        text = f"___________{coin}___________\n" \
               f"profits: USDT -> IRT\n" \
               f"Amount: {buy_in_usdt_sell_in_irt['amount']}\n" \
               f"Buy Price: {buy_in_usdt_sell_in_irt['buy_price']} USDT\n" \
               f"Sell Price: {buy_in_usdt_sell_in_irt['sell_price']} USDT\n" \
               f"USDTIRT price: {Decimal(usdtirt_price)}\n" \
               f"Difference Percentage: {(buy_in_usdt_sell_in_irt['sell_price'] - buy_in_usdt_sell_in_irt['buy_price']) / buy_in_usdt_sell_in_irt['buy_price'] * 100}%\n"
        print(text)
        send_telegram_message_task.delay(text, chat_id)

    if buy_in_irt_sell_in_usdt['buy_price'] < buy_in_irt_sell_in_usdt['sell_price']:
        text = f"___________{coin}___________\n" \
               f"direction: IRT -> USDT\n" \
               f"Amount: {buy_in_irt_sell_in_usdt['amount']}\n" \
               f"Buy Price: {buy_in_irt_sell_in_usdt['buy_price']} IRT\n" \
               f"Sell Price: {buy_in_irt_sell_in_usdt['sell_price']} IRT\n" \
               f"USDTIRT price: {Decimal(usdtirt_price)}\n" \
               f"Difference Percentage: {(buy_in_irt_sell_in_usdt['sell_price'] - buy_in_irt_sell_in_usdt['buy_price']) / buy_in_irt_sell_in_usdt['buy_price'] * 100}%\n"
        print(text)
        send_telegram_message_task.delay(text, chat_id)

@shared_task(name='check_coin_task')
def check_coin_task():
    last_coin_id = cache.get('last_checked_coin_id', 0)
    cache.set('last_checked_coin_id', (last_coin_id + 1) % len(COIN_LIST))
    coin = COIN_LIST[last_coin_id]
    check_coin(coin)

@shared_task(name='send_telegram_message_task')
async def send_telegram_message_task(message, chat_id):
    await send_telegram_message(message, chat_id)