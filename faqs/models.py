""" Models for the faqs app. """
from django.db import models


class FAQ(models.Model):
    """
    Frequently asked question model to provide
    information to customers.
    """
    question = models.CharField(max_length=250)
    answer = models.TextField()

    def __str__(self):
        return self.question
