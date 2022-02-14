""" Views for the contact app. """
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ContactForm
from .models import ContactMessage


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
            return redirect(reverse('home'))
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


@login_required
def manage_contacts(request):
    """
    List customer contact messages for the store owner.
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry this area is for the store owner.')
        return redirect(reverse('home'))

    contact_messages = ContactMessage.objects.all()

    context = {
        'contact_messages': contact_messages
    }

    return render(request, 'contact/manage_contacts.html', context)
