""" Forms for creating an order at checkout. """
from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """
    A form for buying jewellery and creating an order.
    """
    class Meta:
        """ Select the model and define the fields. """
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'address1', 'address2', 'town_or_city',
                  'county', 'postcode', 'country')

    def __init__(self, *args, **kwargs):
        """
        Add placeholders for the fields and autofocus on first field.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postcode',
            'address1': 'Address 1',
            'address2': 'Address 2',
            'town_or_city': 'Town or City',
            'county': 'County'
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False
