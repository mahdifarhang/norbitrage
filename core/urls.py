from django.urls import path

from core.views import *

app_name='core'

urlpatterns = [
    path('market-list', market_list, name='market_list'),
    path('load-orderbook/<str:market>', load_orderbook, name='load_orderbook'),
    path('price-check', check_coin_price_difference, name='check_coin_price_difference'),
]