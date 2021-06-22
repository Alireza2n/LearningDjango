import jdatetime
import pytz
from django.conf import settings
from django.core.management import BaseCommand

from store.enums import OrderStatuses
from store.models import Order


class Command(BaseCommand):
    help = 'Cancels un-completed orders.'

    def handle(self, *args, **options):
        qs = Order.objects.filter(status=OrderStatuses.CREATED)
        for order in qs:
            # Check if they are older than 1 day
            today = jdatetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
            order_date = order.created_on
            diff = today - order_date
            if diff.days > 1:
                order.set_as_canceled()
                print(f"Set Order #{order.pk} as canceled.")
            else:
                print(f"Order #{order.pk} is less than 1 days old.")