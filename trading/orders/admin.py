from django.contrib import admin
from .models import orders_details, balance

"""
    Here the model named orders_details and balance is registered.
    The data listed her are shown on admin pannel.
    """

class orderadmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_type', 'price',
                    'quantity', 'user_id')
    list_display_links = ('order_id',)
    readonly_feilds = ('order_type', 'price',
                       'quantity', 'user_id')
    ordering = ('time_stamp',)
    search_fields = ('order_id',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class baladmin(admin.ModelAdmin):
    list_display = ('balance_id', 'usd_amount',
                    'btc_quantity', 'user_id')
    list_display_links = ('balance_id',)
    readonly_feilds = ('usd_amount',
                       'btc_quantity', 'user_id')
    ordering = ('time_stamp',)
    search_fields = ('balance_id',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(orders_details, orderadmin)
admin.site.register(balance, baladmin)
