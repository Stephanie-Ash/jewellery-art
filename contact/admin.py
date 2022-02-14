""" Admin panel set-up for the contact app. """
from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin options for the ContactMessage model.
    """
    list_display = ('date_created', 'topic', 'email', 'message')
    ordering = ('-date_created',)
