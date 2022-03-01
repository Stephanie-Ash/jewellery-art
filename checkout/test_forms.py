""" Testcases for the checkout app forms. """
from django.test import TestCase
from .forms import OrderForm


class TestForms(TestCase):
    """ Tests for the forms. """
    def test_user_editable_fields_are_required_on_order_form(self):
        """
        Test that the Prder full name, email, phone number, country
        address1 and town or city fields are required on the Order form.
        """
        form = OrderForm(
            {'full_name': '', 'email': '', 'phone_number': '',
             'country': '', 'address1': '', 'town_or_city': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors.keys())
        self.assertIn('email', form.errors.keys())
        self.assertIn('phone_number', form.errors.keys())
        self.assertIn('country', form.errors.keys())
        self.assertIn('address1', form.errors.keys())
        self.assertIn('town_or_city', form.errors.keys())
        self.assertEqual(
            form.errors['full_name'][0], 'This field is required.')
        self.assertEqual(form.errors['email'][0], 'This field is required.')
        self.assertEqual(
            form.errors['phone_number'][0], 'This field is required.')
        self.assertEqual(form.errors['country'][0], 'This field is required.')
        self.assertEqual(
            form.errors['address1'][0], 'This field is required.')
        self.assertEqual(
            form.errors['town_or_city'][0], 'This field is required.')
