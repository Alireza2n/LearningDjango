from django.db import models
from django.utils.translation import ugettext as _

from . import enums


class Product(models.Model):
    """
    Represents a single product
    """
    name = models.CharField(
        max_length=200,
        verbose_name='نام کالا',
        db_index=True
    )
    description = models.TextField(
        verbose_name=_('Description'),
        help_text='متن نمایشی برای توصیف محصول'
    )
    price = models.PositiveIntegerField(default=0, db_index=True)
    qty_in_stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(
        default=False,
        help_text='آیا این محصول فروخته میشود؟'
    )
    type = models.CharField(
        max_length=100,
        choices=enums.ProductTypes.choices
    )

    def __str__(self):
        return self.name

    def can_be_sold(self):
        """
        Can this product be sold?
        :returns: bool
        """
        return self.is_active

    def is_in_stock(self, qty):
        """
        Is product in stock with requested Qty?
        :returns: bool
        """
        return qty <= self.qty_in_stock
