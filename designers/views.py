""" Views for the designers app. """
from django.shortcuts import render

from .models import Designer


def all_designers(request):
    """
    Display all designers.
    """
    designers = Designer.objects.all()

    context = {
        'designers': designers,
        }

    return render(request, 'designers/designers.html', context)
