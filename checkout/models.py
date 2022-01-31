""" Models for the checkout app. """
import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from products.models import Product


class Order(models.Model):
    """
    Order model for keeping track of customer orders.
    """
    order_number = models.CharField(max_length=32, editable=False)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    address1 = models.CharField(max_length=80)
    address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, default=0)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    def _generate_order_number(self):
        """
        Generate random, unique order number.
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total whenever a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum']
        self.delivery_cost = settings.STANDARD_DELIVERY
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override original save method if no order number set.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """
    OrderLineItem model for the individual products attached
    to each order.
    """
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        """
        Override original save method to set lineitem total
        and so update order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
