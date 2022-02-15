""" Views for the faqs app. """
from django.shortcuts import render


def faqs(request):
    """
    A view to return the frequently asked questions page.
    """

    return render(request, 'faqs/faqs.html')
