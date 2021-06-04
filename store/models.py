from django.contrib.auth import get_user_model
from django.db import models
from django_jalali.db import models as jmodels
from django.utils.translation import ugettext as _
from . import enums


class Order(models.Model):
    """
    Represents an order
    """
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    created_on = jmodels.jDateTimeField(auto_now_add=True)
    status = models.CharField(
        verbose_name=_('Status'),
        help_text='وضعیت سفارش',
        choices=enums.OrderStatuses.choices,
        default=enums.OrderStatuses.CREATED,
        max_length=100
    )


class OrderItem(models.Model):
    """
    A single item in the order
    """
    order = models.ForeignKey('store.Order', on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Product', on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(default=1)
    discount = models.FloatField(default=0)
    price = models.PositiveIntegerField()
