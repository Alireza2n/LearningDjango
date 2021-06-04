from django.db import models
from django.utils.translation import ugettext as _
from . import enums


class Product(models.Model):
    """
    Represents a single product
    """
    name = models.CharField(
        max_length=200,
        verbose_name='نام کالا'
    )
    description = models.TextField(
        verbose_name=_('Description'),
        help_text='متن نمایشی برای توصیف محصول'
    )
    qty_in_stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(
        default=False,
        help_text='آیا این محصول فروخته میشود؟'
    )
    type = models.CharField(
        max_length=100,
        choices=enums.ProductTypes.choices
    )
