""" Admin alert email set-up for contact app. """
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_alert_email(order):
    """
    Email an alert to the store admin when an order is created
    containing out of stock products.
    """
    store_email = settings.DEFAULT_FROM_EMAIL
    subject = render_to_string(
        'checkout/confirmation_emails/alert_email_subject.txt',
        {'order': order})
    body = render_to_string(
        'checkout/confirmation_emails/alert_email_body.txt',
        {'order': order})

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [store_email]
    )
