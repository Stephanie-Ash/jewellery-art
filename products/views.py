""" Views for the products app. """
from django.shortcuts import render

from designers.models import Designer
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

        if 'designer' in request.GET:
            designer = request.GET['designer']
            products = products.filter(designer__programmatic_name=designer)
            designer = Designer.objects.filter(programmatic_name=designer)

    context = {
        'products': products,
        'current_category': category,
        'current_designer': designer,
    }

    return render(request, 'products/products.html', context)
