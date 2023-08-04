import math
import base64
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from backend.accounts.models import Account
from django.contrib import messages
from .models import balance, orders_details
import matplotlib.pyplot as plt
import io
import matplotlib
import requests
matplotlib.use('Agg')

"""
    get the value for the form check if the datas are
    as expected or not, the store the record into the 
    necessary database
"""
@login_required(login_url='login')
def buy(request):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        total = float(request.POST['total'])
        current_user = request.user
        user_email = current_user.email
        user_id = Account.objects.get(email=user_email)
        balance_data = balance.objects.filter(
            user_id=user_id).order_by('-time_stamp').first()
        current_usd_amount = balance_data.usd_amount
        current_btc_amount = balance_data.btc_quantity
        if total <= 0:
            messages.error(request, 'Invalid amount')
            return redirect('buy')
        elif current_usd_amount-total <= 0:
            messages.error(request, 'insufficient amount')
            return redirect('buy')
        else:
            up_balance = balance(usd_amount=current_usd_amount-total,
                                 btc_quantity=current_btc_amount+quantity, user_id=user_id)
            up_balance.save()
            new_order = orders_details(
                order_type="Buy", price=total, quantity=quantity, user_id=user_id)
            new_order.save()
            messages.success(request, 'Successful')
    return render(request, "orders/buy.html")


@login_required(login_url='login')
def sell(request):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        total = float(request.POST['total'])
        current_user = request.user
        user_email = current_user.email
        user_id = Account.objects.get(email=user_email)
        balance_data = balance.objects.filter(
            user_id=user_id).order_by('-time_stamp').first()
        current_usd_amount = balance_data.usd_amount
        current_btc_amount = balance_data.btc_quantity
        print(current_btc_amount)
        if total <= 0:
            messages.error(request, 'Invalid amount')
            return redirect('buy')
        elif current_btc_amount-quantity <= 0:
            messages.error(request, 'insufficient BTC')
            return redirect('buy')
        else:
            up_balance = balance(usd_amount=current_usd_amount+total,
                                 btc_quantity=current_btc_amount-quantity, user_id=user_id)
            up_balance.save()
            new_order = orders_details(
                order_type="Sell", price=total, quantity=quantity, user_id=user_id)
            new_order.save()
            messages.success(request, 'Successful')

    return render(request, 'orders/sell.html')

"""
a query is runned to extract the data of users order
and the query result is send into the frontend
"""
@login_required(login_url='login')
def track_order(request):
    current_user = request.user
    user_email = current_user.email
    user_id = Account.objects.get(email=user_email)
    order_data = orders_details.objects.filter(
        user_id=user_id).order_by('-time_stamp')
    context = {
        'order_data': order_data,
    }
    return render(request, 'orders/track_order.html', context)


@login_required(login_url='login')
def dashboard(request):
    """
    The users data is gathered using query and is calculated
    with the realtime price; price being extracted from the 
    binance API and using matplotlib library a line graph is
    ploted againest the 2 different currency"""
    current_user = request.user
    user_email = current_user.email
    user_id = Account.objects.get(email=user_email)
    balance_data = balance.objects.filter(
        user_id=user_id).order_by('-time_stamp')
    balance_data_current = balance.objects.filter(
        user_id=user_id).order_by('-time_stamp').first()
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT" # endpoint of binance url to get binance price
    response = requests.get(url)
    response.raise_for_status()  # Raise exception
    market_data = response.json()
    current_btc = float(balance_data_current.btc_quantity)
    # it is asumed that the user initiall have 200000USD
    absolute_profit = (current_btc * float(market_data['price'])) - 200000.0
    percentage_profit = (absolute_profit / 200000.0) * 100
    decimal_places = 2
    absolute_profit = math.ceil(
        absolute_profit * 10 ** decimal_places) / (10 ** decimal_places) 
    percentage_profit = math.ceil(
        percentage_profit * 10 ** decimal_places) / (10 ** decimal_places)
    balances = list(balance_data)
    timestamps = [balance.time_stamp for balance in balances]
    balances_usd = [balance.usd_amount for balance in balances]
    balances_btc = [balance.btc_quantity for balance in balances]
    changes_usd = [balances_usd[i] - balances_usd[i-1]
                   for i in range(1, len(balances_usd))]
    changes_btc = [balances_btc[i] - balances_btc[i-1]
                   for i in range(1, len(balances_btc))]

    # Creating the plot
    plt.plot(timestamps[1:], changes_usd)
    plt.plot(timestamps[1:], changes_btc)
    plt.xlabel('Time')
    plt.ylabel('Balance Change')
    plt.title('Balance Change over Time')
    plt.yscale('log')
    plt.gcf().autofmt_xdate() # adujusting the formating
    plt.legend(['USD', 'BTC'])
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0) #move cursor to the beginning of the buffer
    image_base64 = base64.b64encode(buffer.getvalue()).decode() #converting image into base64

    context = {
        'percentage_profit': percentage_profit,
        'absolute_profit': absolute_profit,
        'image_base64': image_base64,
        'balance_data': balance_data,
    }
    return render(request, 'orders/dashboard.html', context)
