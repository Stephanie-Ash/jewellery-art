""" Forms for updating a UserProfile. """
from django import forms

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    A form for updating the UserProfile default delivery details.
    """
    class Meta:
        """ Select the model and define the fields. """
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders for the fields and autofocus on first field.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postcode',
            'default_address1': 'Address 1',
            'default_address2': 'Address 2',
            'default_town_or_city': 'Town or City',
            'default_county': 'County'
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False
