""" Views for the products app. """
from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponseRedirect)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from designers.models import Designer, Collection
from profiles.models import UserProfile
from .models import Product, Category, Review
from .forms import ReviewForm, ProductForm


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
    reviews = product.reviews.all()
    other_products = None
    if product.designer:
        other_products = Product.objects.filter(
            designer__id=product.designer.id)
    purchased = False

    if request.user.is_authenticated:
        profile = get_object_or_404(UserProfile, user=request.user)
        orders = profile.orders.all()
        for order in orders:
            for item in order.lineitems.all():
                if item.product.id == product_id:
                    purchased = True

    review_form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'other_products': other_products,
        'review_form': review_form,
        'purchased': purchased,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_review(request, product_id):
    """
    Allow registered users to add a review of a product.
    """
    product = get_object_or_404(Product, pk=product_id)
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            customer_review = review_form.save(commit=False)
            customer_review.product = product
            customer_review.user_profile = profile
            customer_review.save()
            messages.success(request, 'Review successfully added.')
            return redirect(reverse('product_detail', args=[product_id]))
        else:
            messages.error(
               request, 'Failed to add review. Please check the form.')
    else:
        messages.error(request, 'Sorry a form is required to do that')
        return redirect(reverse('product_detail', args=[product_id]))


@login_required
def edit_review(request, review_id):
    """
    Allow registered users to edit a review on their profile page.
    """
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            messages.success(request, 'Successfully updated review.')
            return redirect(reverse('profile'))
        else:
            messages.error(
                request, 'Failed to update review. Please check the form.')
    else:
        messages.error(request, 'Sorry a form is required to do that')
        return redirect(reverse('profile'))


@login_required
def delete_review(request, review_id):
    """
    Allow registered users to delete a review on their profile page.
    """
    review = get_object_or_404(Review, pk=review_id)
    review.delete()
    messages.success(request, 'Review deleted.')
    return redirect(reverse('profile'))


@login_required
def add_product(request):
    """
    Add a product to the store.
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry this area is for the store owner only.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(
                request, 'Successfully added a product to the store.')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
               request, 'Failed to add product. Please check the form.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """
    Edit the details of an individual product.
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry this area is for the store owner only.')

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully updated {product.name}.')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request, f'Failed to update {product.name}. \
                    Please check the form.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}.')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def update_inventory(request, product_id):
    """
    Update the inventory of an individual product.
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry only a store owner can do this.')

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        inventory = request.POST.get('inventory')
        if inventory == '':
            messages.error(
                request, 'Could not update inventory please enter a value.')
            return redirect('products')
        else:
            product.inventory = inventory
            product.save()
            messages.success(
                request, f'The inventory of {product.name} has been updated')
            return redirect('products')
    else:
        messages.error(request, 'Sorry that action is not possible.')


@login_required
def toggle_homepage_featured(request, product_id):
    """
    Toggle the homepage_featured field of an individual product.
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry, only store owners are authorised to do that.')
        return redirect(reverse('home'))

    current_page = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, pk=product_id)
    product.homepage_featured = not product.homepage_featured
    product.save()

    if current_page:
        return HttpResponseRedirect(current_page)
    else:
        return redirect(reverse('products'))


@login_required
def delete_product(request, product_id):
    """
    Delete a product from the store.
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry, only store owners are authorised to do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted.')
    return redirect(reverse('products'))
