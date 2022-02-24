""" Testcases for the designers app models. """
from django.test import TestCase
from .models import Designer, Collection


class TestModels(TestCase):
    """ Tests for the models. """
    def setUp(self):
        self.designer = Designer.objects.create(
            name='Jane Doe', introduction='Test introduction.'
        )
        self.collection = Collection.objects.create(
            designer=self.designer, name='Test Collection'
        )

    def test_designer_string_method_returns_name(self):
        """ Test the Designer model string method. """
        self.assertEqual(str(self.designer), 'Jane Doe')

    def test_collection_string_method_returns_name(self):
        """ Test the Collection model string method. """
        self.assertEqual(str(self.collection), 'Test Collection')
