from django.db import models
from django.utils.translation import ugettext as _


class OrderStatuses(models.TextChoices):
    """
    Statues an order can have
    """
    CREATED = 'CREATED', _('Created')
    COMPLETED = 'COMPLETED', _('Completed')
    CANCELED = 'CANCELED', _('Canceled')
    SUSPENDED = 'SUSPENDED', _('Suspended')
