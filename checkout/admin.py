from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    # allow us to add or edit admin items from the other model
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inLines = (OrderLineItemAdminInline,)
    # add it to the interface so we can modify it

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total',)

    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total',)
    # not absolutely necessary, but allows us to order the list the
    # same as the model rather than django fixing it

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)
    # restrict the list of columns to show only a few key items

    ordering = ('-date',)  # order by latest first


admin.site.register(Order, OrderAdmin)
# other one loaded using the other models
