from django.contrib import admin

from . import models

admin.site.site_header = 'فروشگاه هنری من'


@admin.action(description='فعال کردن کالا')
def set_product_as_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description='غیرفعال کردن کالا')
def set_product_as_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


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
    actions = [
        set_product_as_active,
        set_product_as_inactive
    ]
