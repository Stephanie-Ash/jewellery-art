""" Models for the products app. """
from django.db import models

from designers.models import Designer, Collection
from profiles.models import UserProfile


class Category(models.Model):
    """
    Category model for the different categories
    of jewllery sold.
    """
    name = models.CharField(max_length=254)
    programmatic_name = models.CharField(
        max_length=254, null=False, editable=False)

    class Meta:
        """
        Set the correct plural name.
        """
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the programmatic
        name if it hasn't been set already.
        """
        if not self.programmatic_name:
            self.programmatic_name = self.name.lower().replace(" ", "_")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product model for all the jewellery products sold.
    """
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL)
    designer = models.ForeignKey(
        Designer, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='products')
    collection = models.ForeignKey(
        Collection, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='products')
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    sizing = models.CharField(max_length=254, null=True, blank=True)
    material = models.CharField(max_length=254, null=True, blank=True)
    num_available = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    homepage_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Review model for customer reviews of the jewellery products.
    """
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='reviews')
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=50)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review on {self.product.name} by {self.name}"
