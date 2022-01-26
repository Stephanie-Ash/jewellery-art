""" Context processor for the basket app. """
from django.conf import settings


def basket_contents(request):
    """
    Basket contents context processor to make
    the basket contents and information available to
    all apps.
    """
    basket_items = []
    total = 0
    product_count = 0
    delivery = settings.STANDARD_DELIVERY
    grand_total = delivery + total

    context = {
        'basket_items': basket_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context
