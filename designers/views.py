""" Views for the designers app. """
from django.shortcuts import render, get_object_or_404

from products.models import Product
from .models import Designer, Collection
from .forms import DesignerForm


def all_designers(request):
    """
    Display all designers.
    """
    designers = Designer.objects.all()

    context = {
        'designers': designers,
        }

    return render(request, 'designers/designers.html', context)


def designer_detail(request, designer_id):
    """
    Display the details of an individual designer.
    """
    designer = get_object_or_404(Designer, id=designer_id)
    products = Product.objects.filter(
        designer__id=designer_id).filter(collection=None)
    collections = Collection.objects.filter(designer__id=designer_id)

    context = {
        'designer': designer,
        'products': products,
        'collections': collections,
    }

    return render(request, 'designers/designer_detail.html', context)


def add_designer(request):
    """
    Add a designer to the store.
    """
    form = DesignerForm()

    template = 'designers/add_designer.html'
    context = {
        'form': form,
        'on_management': True
    }

    return render(request, template, context)
