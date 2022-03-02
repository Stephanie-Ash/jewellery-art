""" Models for the faqs app. """
from django.db import models


class FAQ(models.Model):
    """
    Frequently asked question model to provide
    information to customers.
    """
    # Set options for the category field
    ORDER = 'OR'
    DELIVERY = 'DE'
    PRODUCT = 'PR'
    DESIGNER = 'DS'
    ACCOUNT = 'WB'
    OTHER = 'OT'
    CATEGORY_CHOICES = [
        ('', 'Select Category *'),
        (ORDER, 'Orders'),
        (DELIVERY, 'Deliveries'),
        (PRODUCT, 'Products'),
        (DESIGNER, 'Designers'),
        (ACCOUNT, 'Customer Accounts'),
        (OTHER, 'Other'),
    ]

    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    question = models.CharField(max_length=250)
    answer = models.TextField()

    def __str__(self):
        return self.question
