""" Forms for the faqs app. """
from django import forms

from .models import FAQ


class FAQForm(forms.ModelForm):
    """
    A form to add a frequently asked question to
    the site.
    """
    class Meta:
        """ Select the model and define the fields. """
        model = FAQ
        fields = '__all__'
