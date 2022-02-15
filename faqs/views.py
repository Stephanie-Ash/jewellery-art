""" Views for the faqs app. """
from django.shortcuts import render

from .models import FAQ


def faqs(request):
    """
    A view to return the frequently asked questions page.
    """
    questions = FAQ.objects.all()
    categories = questions.values_list('category', flat=True)

    context = {
        'faqs': questions,
        'categories': categories,
    }

    return render(request, 'faqs/faqs.html', context)
