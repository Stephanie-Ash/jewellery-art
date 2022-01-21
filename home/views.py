""" Views for the home app. """
from django.shortcuts import render
from products.models import Product


def index(request):
    """
    A view to return the homepage.
    """
    featured_products = Product.objects.filter(homepage_featured=True)

    context = {
        'featured_products': featured_products,
    }

    return render(request, 'home/index.html', context)
