""" Context processor for the basket app. """
from django.conf import settings
from django.shortcuts import get_object_or_404

from products.models import Product


def basket_contents(request):
    """
    Basket contents context processor to make
    the basket contents and information available to
    all apps.
    """
    basket_items = []
    total = 0
    product_count = 0
    basket = request.session.get('basket', {})
    country = request.session.get('country', '')

    for item_id, quantity in basket.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        product_count += quantity
        basket_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    if total:
        if country:
            if country == 'GB':
                delivery = 0
            else:
                delivery = settings.STANDARD_DELIVERY
        else:
            delivery = settings.STANDARD_DELIVERY
    else:
        delivery = 0

    grand_total = delivery + total

    context = {
        'basket_items': basket_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context
