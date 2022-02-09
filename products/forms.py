""" Forms for the products app. """
from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    """
    A form to add a review on a product.
    """
    class Meta:
        """ Select the model and define the fields. """
        model = Review
        fields = ('name', 'body')

    def __init__(self, *args, **kwargs):
        """ Add placeholder to body field. """
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Name'
        self.fields['body'].widget.attrs['placeholder'] = (
            'Write your review here.')
        for field in self.fields:
            self.fields[field].label = False
