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

    def test_featured_products_length(self):
        """
        Test that the homepage featured products context
        countains all featured products if less than 3 and
        never more than more than 4 products.
        """
        product1 = Product.objects.create(
            name='Test Name1', description='Test description1',
            price=10.00, homepage_featured=True
        )
        product2 = Product.objects.create(
            name='Test Name2', description='Test description2',
            price=10.00, homepage_featured=True
        )
        Product.objects.create(
            name='Test Name3', description='Test description3',
            price=10.00, homepage_featured=True
        )
        Product.objects.create(
            name='Test Name4', description='Test description4',
            price=10.00, homepage_featured=True
        )
        Product.objects.create(
            name='Test Name5', description='Test description5',
            price=10.00, homepage_featured=True
        )

        response = self.client.get('/')
        self.assertEqual(len(response.context['featured_products']), 4)

        product1.homepage_featured = False
        product1.save()
        product2.homepage_featured = False
        product2.save()

        response = self.client.get('/')
        self.assertEqual(len(response.context['featured_products']), 3)
