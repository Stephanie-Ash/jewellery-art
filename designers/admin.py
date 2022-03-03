""" Admin panel set-up for the designers app. """
from django.contrib import admin
from .models import Designer, Collection


@admin.register(Designer)
class DesignerAdmin(admin.ModelAdmin):
    """
    Admin options for the Designer model.
    """
    list_display = ('name', 'phone_number', 'email')
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    """
    Admin options for the Collection model.
    """
    list_display = ('name', 'designer')
    ordering = ('name',)
    search_fields = ('name',)
