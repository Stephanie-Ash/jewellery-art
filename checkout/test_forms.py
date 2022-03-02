""" Testcases for the checkout app forms. """
from django.test import TestCase
from .forms import OrderForm


class TestForms(TestCase):
    """ Tests for the forms. """
    def test_user_editable_fields_are_required_on_order_form(self):
        """
        Test that the Order full name, email, phone number, country
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

    def test_unrequired_fields_not_required_order_form(self):
        """
        Test that the fields not required in the Order model
        objects are not required on the form.
        """
        form = OrderForm(
            {'full_name': 'Name', 'email': 'email@email.com',
             'phone_number': '01234567890', 'country': 'GB',
             'address1': '1 Street', 'town_or_city': 'Town'})
        self.assertTrue(form.is_valid())

    def test_only_user_editable_fields_in_form_metaclass(self):
        """ Test that only the fields the user can edit are on the form """
        form = OrderForm()
        self.assertEqual(
            form.Meta.fields,
            ('full_name', 'email', 'phone_number', 'address1', 'address2',
             'town_or_city', 'county', 'postcode', 'country'))
