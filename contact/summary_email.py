""" Confirmation email set-up for contact app. """
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_summary_email(contact_message):
    """
    Email a summary of the submitted contact form to
    the site user.
    """
    contact_email = contact_message.email
    subject = render_to_string(
        'contact/summary_emails/summary_email_subject.txt')
    body = render_to_string(
        'contact/summary_emails/summary_email_body.txt',
        {'contact_message': contact_message})

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [contact_email]
    )
