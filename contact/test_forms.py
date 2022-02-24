""" Testcases for the contact app forms. """
from django.test import TestCase
from .forms import ContactForm


class TestForms(TestCase):
    """ Tests for the forms. """
    def test_ensure_fields_are_required(self):
        """
        Test that the ContactMessage required model fields are
        required on the form.
        """
        form = ContactForm(
            {
                'topic': '',
                'first_name': '',
                'last_name': '',
                'email': '',
                'message': ''
            })
        self.assertFalse(form.is_valid())
        self.assertIn('topic', form.errors.keys())
        self.assertIn('first_name', form.errors.keys())
        self.assertIn('last_name', form.errors.keys())
        self.assertIn('email', form.errors.keys())
        self.assertIn('message', form.errors.keys())
        self.assertEqual(form.errors['topic'][0], 'This field is required.')
        self.assertEqual(
            form.errors['first_name'][0], 'This field is required.')
        self.assertEqual(
            form.errors['last_name'][0], 'This field is required.')
        self.assertEqual(form.errors['email'][0], 'This field is required.')
        self.assertEqual(form.errors['message'][0], 'This field is required.')

    def test_phone_number_field_not_required(self):
        """
        Test that the phone_number field is not required on the form.
        """
        form = ContactForm(
            {
                'topic': 'OR',
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'email@email.com',
                'message': 'Message'
            })
        self.assertTrue(form.is_valid())

    def test_only_user_editable_fields_in_form_metaclass(self):
        """ Test that only the fields the user can edit are on the form """
        form = ContactForm()
        self.assertEqual(
            form.Meta.fields,
            ('topic', 'first_name', 'last_name', 'email', 'phone_number',
             'message'))
