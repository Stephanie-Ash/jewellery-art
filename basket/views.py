""" Views for the basket app. """
from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404)
from django.contrib import messages

from products.models import Product
from profiles.models import UserProfile
from checkout.forms import OrderForm
from .inventory_check import check_inventory


def view_basket(request):
    """
    Display the shopping basket and its contents.
    """
    out_of_stock = check_inventory(request)
    if out_of_stock:
        messages.warning(
            request, f'There are no longer enough of the following item(s) in \
                stock and they have been removed from your basket: \
                    {", ".join([str(x) for x in [*out_of_stock]])}')

    referring_page = request.META.get('HTTP_REFERER')
    if referring_page:
        if 'basket' not in referring_page:
            if 'country' in request.session:
                del request.session['country']

    country_code = request.session.get('country', '')

    if country_code:
        order_form = OrderForm(initial={
            'country': country_code,
        })
    elif request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            order_form = OrderForm(initial={
                'country': profile.default_country,
            })
            country_code = f'{profile.default_country}'
            request.session['country'] = country_code
        except UserProfile.DoesNotExist:
            order_form = OrderForm()
    else:
        order_form = OrderForm()

    context = {
        'form': order_form,
        'country_code': country_code,
    }

    return render(request, 'basket/basket.html', context)


def add_to_basket(request, item_id):
    """
    Add a product to the basket.
    """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    basket = request.session.get('basket', {})

    if item_id in list(basket.keys()):
        current_quantity = basket[item_id]
        if current_quantity + quantity <= product.inventory:
            basket[item_id] += quantity
            messages.success(
                request, f'Updated the quantity of {product.name} in your \
                    basket.', extra_tags='basket')
        else:
            messages.error(
                request, f'There are not enough in stock to add more of \
                    this item to your basket. Quantity in basket: \
                    {current_quantity}, \
                    Quantity in stock: {product.inventory}')
    else:
        if quantity <= product.inventory:
            basket[item_id] = quantity
            messages.success(
                request, f'Added {product.name} to your basket.',
                extra_tags='basket')
        else:
            messages.error(
                request, f'There are only {product.inventory} of {product.name} \
                    in stock and so not enough to add this item \
                    to your basket')

    request.session['basket'] = basket
    return redirect(redirect_url)


def adjust_basket(request, item_id):
    """
    Adjust the quantity of a product in the basket.
    """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    basket = request.session.get('basket', {})

    if quantity > 0:
        basket[item_id] = quantity
        messages.success(
            request, f'Updated the quantity of {product.name} in your basket.',
            extra_tags='basket')
    else:
        basket.pop(item_id)
        messages.success(
            request, f'Removed {product.name} from your basket.',
            extra_tags='basket')

    request.session['basket'] = basket
    return redirect(reverse("view_basket"))


def remove_from_basket(request, item_id):
    """
    Remove a product from the basket.
    """
    try:
        product = get_object_or_404(Product, pk=item_id)
        basket = request.session.get('basket', {})

        basket.pop(item_id)
        messages.success(
            request, f'Removed {product.name} from your basket.',
            extra_tags='basket')

        request.session['basket'] = basket
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)


def set_delivery_country(request, country_code):
    """
    Set the delivery country so that the delivery price can
    be calculated
    """
    if country_code == 'no_country':
        if 'country' in request.session:
            del request.session['country']
    else:
        request.session['country'] = country_code

    return HttpResponse(status=200)
