""" Testcases for the home app views. """
from django.test import TestCase
from products.models import Product


class TestViews(TestCase):
    """ Tests for the views"""

    def test_get_index_page(self):
        """ Test the index page view loads. """
        Product.objects.create(
            name='Test Name', description='Test description',
            price=10.00
        )
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
