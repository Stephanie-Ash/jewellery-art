""" Admin panel set-up for the faqs app. """
from django.contrib import admin
from .models import FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """
    Admin options for the FAQ model.
    """
    list_display = ('category', 'question', 'answer')
    ordering = ('category',)
