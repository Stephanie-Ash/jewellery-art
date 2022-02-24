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
