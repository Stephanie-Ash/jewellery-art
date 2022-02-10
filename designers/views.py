""" Views for the designers app. """
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

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
    if request.method == 'POST':
        form = DesignerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Successfully added a designer to the store.')
            return redirect(reverse('add_designer'))
        else:
            messages.error(
               request, 'Failed to add designer. Please check the form.')
    else:
        form = DesignerForm()

    template = 'designers/add_designer.html'
    context = {
        'form': form,
        'on_management': True
    }

    return render(request, template, context)
