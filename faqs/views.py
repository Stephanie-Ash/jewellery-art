""" Views for the faqs app. """
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import FAQ
from .forms import FAQForm


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


@login_required
def add_faq(request):
    """
    Add a FAQ to the store.
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry this area is for the store owner only.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Successfully added a FAQ to the FAQs page.')
            return redirect(reverse('faqs'))
        else:
            messages.error(
               request, 'Failed to add FAQ. Please check the form.')
    else:
        form = FAQForm()

    template = 'faqs/add_faq.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
