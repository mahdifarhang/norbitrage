from django.urls import path

from core.views import *

app_name='core'

urlpatterns = [
    path('load-orderbook/<str:market>', load_orderbook, name='load_orderbook'),
]