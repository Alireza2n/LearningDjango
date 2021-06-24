from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save)
def send_email_when_order_is_placed(sender, **kwargs):
    """
    A call back for sending email when order is placed.
    """
    if "store.models.Order'" in str(sender):
        print("Hello from signals.")
