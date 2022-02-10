""" Views for the home app. """
import random

from django.shortcuts import render
from products.models import Product


def index(request):
    """
    A view to return the homepage.
    """
    all_featured = list(Product.objects.filter(homepage_featured=True))
    if len(all_featured) > 4:
        featured_products = random.sample(all_featured, 4)
    else:
        featured_products = all_featured

    context = {
        'featured_products': featured_products,
    }

    return render(request, 'home/index.html', context)
