""" Testcases for the designer app forms. """
from django.test import TestCase
from .forms import DesignerForm


class TestForms(TestCase):
    """ Tests for the forms. """
    def test_ensure_fields_are_required(self):
        """
        Test that the Designer name and introduction fields are
        required on the form.
        """
        form = DesignerForm({'name': '', 'introduction': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())
        self.assertIn('introduction', form.errors.keys())
        self.assertEqual(form.errors['name'][0], 'This field is required.')
        self.assertEqual(
            form.errors['introduction'][0], 'This field is required.')

    def test_unrequired_fields_not_required(self):
        """
        Test that the fields not required in the Designer model
        objects are not required on the form.
        """
        form = DesignerForm({'name': 'Some Name', 'introduction': 'Intro'})
        self.assertTrue(form.is_valid())

    def test_non_editable_fields_not_in_form_metaclass(self):
        """ Test that the programmatice name field is not on the form. """
        form = DesignerForm()
        self.assertNotIn('programmatic_name', form.Meta.fields)
