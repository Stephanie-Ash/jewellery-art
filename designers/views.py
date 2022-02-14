""" Views for the designers app. """
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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


@login_required
def add_designer(request):
    """
    Add a designer to the store.
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry, only store owners are authorised to do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = DesignerForm(request.POST, request.FILES)
        if form.is_valid():
            designer = form.save()
            messages.success(
                request, 'Successfully added a designer to the store.')
            return redirect(reverse('designer_detail', args=[designer.id]))
        else:
            messages.error(
               request, 'Failed to add designer. Please check the form.')
    else:
        form = DesignerForm()

    template = 'designers/add_designer.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_designer(request, designer_id):
    """
    Edit the details of an individual designer.
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry, only store owners are authorised to do that.')
        return redirect(reverse('home'))

    designer = get_object_or_404(Designer, pk=designer_id)
    if request.method == 'POST':
        form = DesignerForm(request.POST, request.FILES, instance=designer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully updated {designer.name}.')
            return redirect(reverse('designer_detail', args=[designer.id]))
        else:
            messages.error(
                request, f'Failed to update {designer.name}. \
                    Please check the form.')
    else:
        form = DesignerForm(instance=designer)
        messages.info(request, f'You are editing {designer.name}.')

    template = 'designers/edit_designer.html'
    context = {
        'form': form,
        'designer': designer,
    }

    return render(request, template, context)


@login_required
def delete_designer(request, designer_id):
    """
    Delete a designer from the store.
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry, only store owners are authorised to do that.')
        return redirect(reverse('home'))

    designer = get_object_or_404(Designer, pk=designer_id)
    designer.delete()
    messages.success(request, 'Designer deleted.')
    return redirect(reverse('designers'))
