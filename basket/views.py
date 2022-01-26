""" Views for the basket app. """
from django.shortcuts import render


def view_basket(request):
    """
    Display the shopping basket and its contents.
    """

    return render(request, 'basket/basket.html')
