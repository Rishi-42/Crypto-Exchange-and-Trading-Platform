from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required

"""
The user need to log in before visiting the website
using the rapidapi endpoint url the market data is collected
the header dict is the api credentials"""
@login_required(login_url='login')
def market_data_view(request):
    url = "https://coinpaprika1.p.rapidapi.com/coins/btc-bitcoin/markets"

    headers = {
        "X-RapidAPI-Key": "5f22f022b4msh5c9d7483e3ec13cp138b95jsna2eb5fadd5eb",
        "X-RapidAPI-Host": "coinpaprika1.p.rapidapi.com"
    }

    return render(request, 'market/market.html', {'url': url, 'headers': headers})
