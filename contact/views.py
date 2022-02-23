""" Views for the contact app. """
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ContactForm
from .models import ContactMessage
from .summary_email import send_summary_email


def contact(request):
    """
    A view to return the contact page.
    """
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_message = contact_form.save()
            send_summary_email(contact_message)
            messages.success(
                request, f'Thank you for your message. \
                    A summary has been sent to {contact_message.email}. \
                    We will get back to you as soon as we can.')
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
            request, 'Sorry this area is for the store owner only.')
        return redirect(reverse('home'))

    contact_messages = ContactMessage.objects.all()

    context = {
        'contact_messages': contact_messages
    }

    return render(request, 'contact/manage_contacts.html', context)


@login_required
def toggle_responded(request, contact_message_id):
    """
    Toggle the responded field of an individual contact message.
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry, only store owners are authorised to do that.')
        return redirect(reverse('home'))

    contact_message = get_object_or_404(ContactMessage, pk=contact_message_id)
    contact_message.responded = not contact_message.responded
    contact_message.save()

    return redirect(reverse('manage_contacts'))
