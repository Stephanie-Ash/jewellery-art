""" Template tags for the product model """
from django import template
from ..models import Category


register = template.Library()


@register.simple_tag()
def all_categories():
    """
    Make the category objects available in the
    base.html template.
    """

    return Category.objects.all()
