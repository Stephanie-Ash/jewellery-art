"""
Signals for the checkout app to update order totals
when lineitems are added or deleted.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update the order total when a lineitem is updated or created.
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update the order total when a lineitem is deleted.
    """
    instance.order.update_total()
