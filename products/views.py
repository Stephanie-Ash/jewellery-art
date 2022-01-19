""" Views for the products app. """
from django.shortcuts import render
from .models import Product, Category


def all_products(request):
    """
    View to display all products.
    This will include filtering, sorting and searching.
    """
    products = Product.objects.all()
    category = None
    designer = None

    if request.GET:
        if 'category' in request.GET:
            category = request.GET['category']
            products = products.filter(category__programmatic_name=category)
            category = Category.objects.filter(programmatic_name=category)

    context = {
        'products': products,
        'current_category': category
    }

    return render(request, 'products/products.html', context)
