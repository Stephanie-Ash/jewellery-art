""" Views for the contact app. """
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ContactForm


def contact(request):
    """
    A view to return the contact page.
    """
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(
                request, 'Thank you for your message. We will get back to you \
                    as soon as we can.')
            return redirect('home')
        else:
            messages.error(
                request, 'It has not been possible to submit your message. \
                    Please check the form.')
    else:
        contact_form = ContactForm()

    context = {
        'contact_form': contact_form,
    }

    return render(request, 'contact/contact.html', context)
