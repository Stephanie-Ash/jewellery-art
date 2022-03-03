""" Template tags for the products app. """
from django import template
from ..models import Category


register = template.Library()


@register.simple_tag()
def all_categories():
    """
    Make the Category objects available in the
    base.html template.
    """
    return Category.objects.all().order_by('id')
