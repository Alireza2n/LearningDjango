from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _
from django_jalali.db import models as jmodels

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

    def __str__(self):
        return f'Order #{self.pk} for {self.owner.get_full_name()}'

    def get_formatted_date(self):
        return self.created_on.strftime('%Y-%m-%d')

    # @property
    @cached_property
    def formatted_date(self):
        return self.get_formatted_date()

    def set_as_canceled(self):
        self.status = enums.OrderStatuses.CANCELED
        self.save()


class OrderItem(models.Model):
    """
    A single item in the order
    """
    order = models.ForeignKey('store.Order', on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Product', on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(default=1)
    discount = models.FloatField(default=0)
    price = models.PositiveIntegerField()
