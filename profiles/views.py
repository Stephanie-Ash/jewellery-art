""" Views for the profiles app. """
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from checkout.models import Order
from products.forms import ReviewForm
from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile(request):
    """
    Display the user profile.
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile successfully updated.')
        else:
            messages.error(
                request, 'Profile update failed. Please check the form.')
    else:
        form = UserProfileForm(instance=profile)

    orders = profile.orders.all().order_by('-date')
    reviews = profile.reviews.all().order_by('-created_on')
    products = []
    review_form = ReviewForm()

    for order in orders:
        # Select previously purchased products
        for item in order.lineitems.all():
            products.append(item.product)
    # Ensure products only appear once
    purchased_products = list(dict.fromkeys(products))

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'reviews': reviews,
        'purchased_products': purchased_products,
        'review_form': review_form,
    }

    return render(request, template, context)


def order_history(request, order_number):
    """
    View the order confirmation for a selected order.
    """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past order confirmation for order number {order_number}.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
