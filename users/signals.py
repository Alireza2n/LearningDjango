from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from store.signals import order_placed
from users.models import Profile


@receiver(order_placed)
def send_email_when_order_is_placed(sender, **kwargs):
    """
    A call back for sending email when order is placed.
    """
    print(f"Hello from signals. {kwargs['created']}")


@receiver(post_save, sender=get_user_model())
def create_profile_for_new_users(sender, **kwargs):
    """
    Creates profile for new users
    """
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])
