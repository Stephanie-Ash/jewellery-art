""" Template tags for the basket app. """
from django import template


register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """
    Calculate the subtotal of each basket item
    and make it available as a filter for all templates.
    """
    return price * quantity
