""" Forms for the contact app. """
from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """
    A form to add a customer contact message.
    """
    class Meta:
        """ Select the model and define the fields. """
        model = ContactMessage
        fields = ('topic', 'first_name', 'last_name',
                  'email', 'phone_number', 'message')

    def __init__(self, *args, **kwargs):
        """ Add placeholders to fields. """
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'message': 'Add your comment or query here.'
        }

        for field in self.fields:
            if field != 'topic':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False
