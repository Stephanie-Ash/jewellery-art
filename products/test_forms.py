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
