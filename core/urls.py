from django.urls import path

from core.views import *

app_name='core'

urlpatterns = [
    path('market-list', market_list, name='market_list'),
    path('load-orderbook/<str:market>', load_orderbook, name='load_orderbook'),
]