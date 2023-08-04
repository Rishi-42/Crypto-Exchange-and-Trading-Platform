from django.urls import path
from .views import *

urlpatterns = [
    path('', market_data_view, name="market_data_view"),
]
