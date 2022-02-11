""" Forms for the designers app. """
from django import forms

from products.widgets import CustomClearableFileInput
from .models import Designer


class DesignerForm(forms.ModelForm):
    """
    A form to add or update designers in the store.
    """
    class Meta:
        """ Select the model and define the fields. """
        model = Designer
        fields = ('name', 'introduction', 'phone_number',
                  'email', 'website_link', 'facebook_link',
                  'instagram_link', 'twitter_link', 'image')

    image = forms.ImageField(
        label='image', required=False, widget=CustomClearableFileInput)
