""" Views for the products app. """
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from designers.models import Designer, Collection
from .models import Product, Category


def all_products(request):
    """
    Display all products.
    This will include filtering, sorting and searching.
    """
    products = Product.objects.all()
    all_categories = Category.objects.all()
    category = None
    designer = None
    collection = None
    sort = None
    direction = None
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Please enter some search criteria!")
                return redirect(reverse('products'))
            queries = Q(
                name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

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
        'search_term': query,
        'categories': all_categories
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    Display the details of an individual product.
    """
    product = get_object_or_404(Product, id=product_id)
    other_products = None
    if product.designer:
        other_products = Product.objects.filter(designer__id=product.designer.id)

    context = {
        'product': product,
        'other_products': other_products,
    }

    return render(request, 'products/product_detail.html', context)
