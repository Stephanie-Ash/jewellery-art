""" Admin panel set-up for the products app. """
from django.contrib import admin
from .models import Category, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin options for the Category model.
    """
    list_display = ('name', 'programmatic_name')
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin options for the Product model.
    """
    list_display = (
        'sku', 'name', 'category', 'collection', 'designer', 'price', 'image')
    ordering = ('sku',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin options for the Product model.
    """
    list_display = ('product', 'name', 'body', 'created_on')
    ordering = ('-created_on',)
