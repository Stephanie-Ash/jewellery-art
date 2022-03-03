""" Template tags for the designers app. """
from django import template
from ..models import Designer, Collection


register = template.Library()


@register.simple_tag()
def all_designers():
    """
    Make the Designer objects available in the
    base.html template.
    """
    return Designer.objects.all().order_by('id')


@register.simple_tag()
def all_collections():
    """
    Make the Collection objects available in the
    base.html template.
    """
    return Collection.objects.all().order_by('id')
