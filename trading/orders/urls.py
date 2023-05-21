from django.urls import path
from .views import *

urlpatterns = [
    path('buy/', buy, name="buy"),
    path('sell/', sell, name="sell"),
    path('track_order/', track_order, name='track_order'),
    path('dashboard/', dashboard, name='dashboard'),
]
