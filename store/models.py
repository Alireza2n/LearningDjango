import logging

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum, F
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django_jalali.db import models as jmodels

from . import enums
from .signals import order_placed

logger = logging.getLogger(__name__)


class OrderQuerySetManager(models.QuerySet):
    """
    Custom QuerySet Manager
    """

    def filter_by_owner(self, user):
        """
        Filters objects by owner field
        """
        return self.filter(owner=user)


class Order(models.Model):
    """
    Represents an order
    """
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name=_('ثبت کننده سفارش'))
    created_on = jmodels.jDateTimeField(auto_now_add=True, verbose_name=_('تاریخ ثبت'))
    status = models.CharField(
        verbose_name=_('وضعیت'),
        help_text=_('وضعیت سفارش'),
        choices=enums.OrderStatuses.choices,
        default=enums.OrderStatuses.CREATED,
        max_length=100
    )

    objects = OrderQuerySetManager.as_manager()

    def __str__(self):
        return f'Order #{self.pk} for {self.owner.get_full_name()}'

    def get_formatted_date(self):
        return self.created_on.strftime('%Y-%m-%d')

    # @property
    @cached_property
    def formatted_date(self):
        return self.get_formatted_date()

    def set_as_canceled(self):
        """
        Sets the order as canceled
        """
        self.status = enums.OrderStatuses.CANCELED
        self.save()
        logger.info(f'Order #{self.pk} was set as CANCELED.')

    def save(self, **kwargs):
        # Is this object new or edited
        if self.pk is None:
            created = True
        else:
            created = False

        super().save(**kwargs)

        # Dispatch order_placed signed
        order_placed.send(
            sender=self.__class__,
            instance=self,
            created=created
        )
        logger.debug(f'order_placed signal was sent for Order #{self.pk}.')

    def get_total_qty(self):
        """
        Sums total qty of related order items in PYTHON
        (which is inefficient)
        """
        # t = 0
        # for item in self.orderitem_set.all():
        #     t += item.qty
        # return t
        return self.orderitem_set.aggregate(Sum('qty')).get('qty__sum', 0)

    def get_item_rows(self):
        return self.orderitem_set.count()

    def get_grand_total(self):
        """
        Returns grand total of Order
        """
        # Using pythin
        # t = 0
        # for item in self.orderitem_set.all():
        #     t += item.qty * item.price
        # return t

        # Using aggregate and annotate
        return self.orderitem_set.all().annotate(grand_total=F('qty') * F('price')) \
            .aggregate(Sum('grand_total'))['grand_total__sum']


class OrderItem(models.Model):
    """
    A single item in the order
    """
    order = models.ForeignKey('store.Order', on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Product', on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(default=1, verbose_name=_('تعداد'))
    discount = models.FloatField(default=0, verbose_name=_('تخفیف'))
    price = models.PositiveIntegerField(verbose_name=_('قیمت'))

    def get_total(self):
        return self.qty * self.price
