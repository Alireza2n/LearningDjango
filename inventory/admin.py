from django.contrib import admin

from . import models

admin.site.site_header = 'فروشگاه هنری من'


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'description',
        'price',
        'qty_in_stock',
        'is_active',
        'type',
    )
    list_display_links = (
        'pk',
        'name',
    )
    list_editable = (
        'price',
        'qty_in_stock',
    )
    search_fields = (
        'name',
        'description__icontains',
    )
    list_filter = (
        'is_active',
        'type',
    )
