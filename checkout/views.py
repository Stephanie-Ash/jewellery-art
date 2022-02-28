""" Views for the checkout app. """
import json
import stripe

from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.db import IntegrityError

from basket.contexts import basket_contents
from basket.inventory_check import check_inventory
from products.models import Product
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from .models import OrderLineItem, Order
from .forms import OrderForm


def login_or_guest(request):
    """
    Display sign in or guest page pre checkout.
    """

    return render(request, 'checkout/login_or_guest.html')


@require_POST
def update_inventory(request):
    """
    Update the inventory of the basket products on checkout form
    submission. If not enough inventory reset inventory and refresh page.
    """
    basket = request.session.get('basket', {})
    original_inventory = {}
    products = {}
    for item_id, quantity in basket.items():
        product = Product.objects.get(id=item_id)
        original_inventory[item_id] = product.inventory
        products[item_id] = product

    try:
        for item_id, quantity in basket.items():
            product = products[item_id]
            product.inventory -= quantity
            product.save()
        return HttpResponse(status=200)
    except IntegrityError as e:
        for item_id, quantity in basket.items():
            product = products[item_id]
            product.inventory = original_inventory[item_id]
            product.save()
        messages.error(
            request, 'Sorry your payment could not be processed due to \
                out of stock items.')
        return HttpResponse(content=e, status=400)


@require_POST
def cache_checkout_data(request):
    """
    Cache checkout data to allow order to be saved when creating
    an order from the webhook.
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('basket', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment could not be processed. \
            Please try again.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
    Display order form and checkout.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    country_code = request.session.get('country', '')

    if request.method == 'POST':
        basket = request.session.get('basket', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'phone_number': request.POST['phone_number'],
            'email': request.POST['email'],
            'address1': request.POST['address1'],
            'address2': request.POST['address2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'postcode': request.POST['postcode'],
            'country': country_code,
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_basket = json.dumps(basket)
            order.save()
            for item_id, quantity in basket.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "A product in your basket wasn't found \
                            in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_basket'))
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse(
                'checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please check the information provided.')
    else:
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "Your basket is currently empty.")
            return redirect(reverse('products'))

        out_of_stock = check_inventory(request)
        if out_of_stock:
            messages.warning(
                request, f'There are no longer enough of the following item(s) in \
                    stock and they have been removed from your basket: \
                        {", ".join([str(x) for x in [*out_of_stock]])}')
            return redirect(reverse('checkout'))

        current_basket = basket_contents(request)
        total = current_basket['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if country_code:
            if request.user.is_authenticated:
                try:
                    profile = UserProfile.objects.get(user=request.user)
                    order_form = OrderForm(initial={
                        'full_name': profile.user.get_full_name(),
                        'email': profile.user.email,
                        'phone_number': profile.default_phone_number,
                        'country': country_code,
                        'postcode': profile.default_postcode,
                        'town_or_city': profile.default_town_or_city,
                        'address1': profile.default_address1,
                        'address2': profile.default_address2,
                        'county': profile.default_county,
                    })
                except UserProfile.DoesNotExist:
                    order_form = OrderForm(initial={
                        'country': country_code,
                    })
            else:
                order_form = OrderForm(initial={
                    'country': country_code,
                })
        else:
            if request.user.is_authenticated:
                try:
                    profile = UserProfile.objects.get(user=request.user)
                    if profile.default_country:
                        order_form = OrderForm(initial={
                            'full_name': profile.user.get_full_name(),
                            'email': profile.user.email,
                            'phone_number': profile.default_phone_number,
                            'country': profile.default_country,
                            'postcode': profile.default_postcode,
                            'town_or_city': profile.default_town_or_city,
                            'address1': profile.default_address1,
                            'address2': profile.default_address2,
                            'county': profile.default_county,
                        })
                        country_code = f'{profile.default_country}'
                        request.session['country'] = country_code
                    else:
                        country_code = 'GB'
                        request.session['country'] = country_code
                        order_form = OrderForm(initial={
                            'full_name': profile.user.get_full_name(),
                            'email': profile.user.email,
                            'phone_number': profile.default_phone_number,
                            'country': country_code,
                            'postcode': profile.default_postcode,
                            'town_or_city': profile.default_town_or_city,
                            'address1': profile.default_address1,
                            'address2': profile.default_address2,
                            'county': profile.default_county,
                        })
                except UserProfile.DoesNotExist:
                    country_code = 'GB'
                    request.session['country'] = country_code
                    order_form = OrderForm(initial={
                        'country': country_code,
                    })
            else:
                country_code = 'GB'
                request.session['country'] = country_code
                order_form = OrderForm(initial={
                    'country': country_code,
                })

    if not stripe_public_key:
        messages.warning(
            request, 'Stripe public key is missing. \
                Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Confirm order on successful checkout.
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        # Attach user profile to the order.
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

        # Save user delivery info
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_town_or_city': order.town_or_city,
                'default_address1': order.address1,
                'default_address2': order.address2,
                'default_county': order.county,
                'default_postcode': order.postcode,
                'default_country': order.country,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Good news, your order was successful. \
        Your order number is: {order_number}. A confirmation has been \
        sent to {order.email}')

    if 'basket' in request.session:
        del request.session['basket']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
