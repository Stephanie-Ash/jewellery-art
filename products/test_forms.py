""" Testcases for the products app forms. """
from django.test import TestCase
from .forms import ProductForm, ReviewForm


class TestForms(TestCase):
    """ Tests for the forms. """
    def test_ensure_fields_are_required_on_product_form(self):
        """
        Test that the Product name, description, inventory and price
        fields are required on the Product form.
        """
        form = ProductForm(
            {'name': '', 'description': '', 'inventory': '', 'price': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())
        self.assertIn('description', form.errors.keys())
        self.assertIn('inventory', form.errors.keys())
        self.assertIn('price', form.errors.keys())
        self.assertEqual(form.errors['name'][0], 'This field is required.')
        self.assertEqual(
            form.errors['description'][0], 'This field is required.')
        self.assertEqual(
            form.errors['inventory'][0], 'This field is required.')
        self.assertEqual(form.errors['price'][0], 'This field is required.')

    def test_ensure_fields_are_required_on_review_form(self):
        """
        Test that the Review name and body fields are required on the
        Review form.
        """
        form = ReviewForm({'name': '', 'body': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())
        self.assertIn('body', form.errors.keys())
        self.assertEqual(form.errors['name'][0], 'This field is required.')
        self.assertEqual(form.errors['body'][0], 'This field is required.')

    def test_unrequired_fields_not_required_product_form(self):
        """
        Test that the fields not required in the Product model
        objects are not required on the form.
        """
        form = ProductForm(
            {'name': 'Some Name', 'description': 'Describe.',
             'inventory': 1, 'price': 10.00})
        self.assertTrue(form.is_valid())
