""" Views for the home app. """
import random

from django.shortcuts import render
from products.models import Product


def index(request):
    """
    A view to return the homepage.
    """
    all_featured = list(Product.objects.filter(homepage_featured=True))
    if all_featured:
        # If more than 4 featured products select a random selection of 4
        if len(all_featured) > 4:
            featured_products = random.sample(all_featured, 4)
        else:
            featured_products = all_featured
    else:
        # If no featured products select the first 4 products
        featured_products = Product.objects.all()[:4]

    context = {
        'featured_products': featured_products,
    }

    return render(request, 'home/index.html', context)


def privacy_policy(request):
    """
    Display the privacy policy for the site.
    """

    return render(request, 'home/privacy_policy.html')
