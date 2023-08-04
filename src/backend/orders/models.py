from django.db import models
from backend.accounts.models import Account
import uuid


class orders_details(models.Model):
    order_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    order_type = models.CharField(max_length=3, blank=False)
    price = models.IntegerField()
    quantity = models.IntegerField()
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)


class balance(models.Model):
    balance_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    usd_amount = models.IntegerField()
    btc_quantity = models.IntegerField()
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
