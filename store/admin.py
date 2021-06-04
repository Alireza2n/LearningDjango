from django.contrib import admin
from . import models


class OrderItemInline(admin.TabularInline):
    """
    Admin inline for OrderItem model
    """
    model = models.OrderItem
    fields = (
        'product',
        'qty',
        'price',
    )


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (
        OrderItemInline,
    )
