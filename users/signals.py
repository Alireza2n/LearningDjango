# from django.db.models.signals import post_save
from store.signals import order_placed
from django.dispatch import receiver


@receiver(order_placed)
def send_email_when_order_is_placed(sender, **kwargs):
    """
    A call back for sending email when order is placed.
    """
    print(f"Hello from signals. {kwargs['created']}")
