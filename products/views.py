""" Views for the products app. """
from django.shortcuts import render
from django.db.models.functions import Lower

from designers.models import Designer, Collection
from .models import Product, Category


def all_products(request):
    """
    View to display all products.
    This will include filtering, sorting and searching.
    """
    products = Product.objects.all()
    category = None
    designer = None
    collection = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if sortkey == 'designer':
                sortkey = 'designer__name'
            if sortkey == 'collection':
                sortkey = 'collection__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            category = request.GET['category']
            products = products.filter(category__programmatic_name=category)
            category = Category.objects.filter(programmatic_name=category)

        if 'designer' in request.GET:
            designer = request.GET['designer']
            products = products.filter(designer__programmatic_name=designer)
            designer = Designer.objects.filter(programmatic_name=designer)

        if 'collection' in request.GET:
            collection = request.GET['collection']
            products = products.filter(
                collection__programmatic_name=collection)
            collection = Collection.objects.filter(
                programmatic_name=collection)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'current_category': category,
        'current_designer': designer,
        'current_collection': collection,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)
