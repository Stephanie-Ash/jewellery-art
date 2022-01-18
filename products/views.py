""" Views for the products app. """
from django.shortcuts import render
from .models import Product


def all_products(request):
    """
    View to display all products.
    This will include filtering, sorting and searching.
    """
    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)
