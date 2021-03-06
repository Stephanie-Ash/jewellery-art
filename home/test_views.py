""" Testcases for the home app views. """
from django.test import TestCase
from products.models import Product


class TestViews(TestCase):
    """ Tests for the views. """

    def test_get_index_page(self):
        """ Test the index page loads. """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_get_privacy_policy_page(self):
        """ Test the privacy policy page loads. """
        response = self.client.get('/privacy_policy/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/privacy_policy.html')

    def test_featured_products_length(self):
        """
        Test that the homepage featured products context always exists,
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
        product3 = Product.objects.create(
            name='Test Name3', description='Test description3',
            price=10.00, homepage_featured=True
        )
        product4 = Product.objects.create(
            name='Test Name4', description='Test description4',
            price=10.00, homepage_featured=True
        )
        product5 = Product.objects.create(
            name='Test Name5', description='Test description5',
            price=10.00, homepage_featured=True
        )

        response = self.client.get('/')
        # No more thank 4 products included
        self.assertEqual(len(response.context['featured_products']), 4)

        product1.homepage_featured = False
        product1.save()
        product2.homepage_featured = False
        product2.save()

        response = self.client.get('/')
        # All featured included if less than 4
        self.assertEqual(len(response.context['featured_products']), 3)

        product3.homepage_featured = False
        product3.save()
        product4.homepage_featured = False
        product4.save()
        product5.homepage_featured = False
        product5.save()

        response = self.client.get('/')
        # First 4 products included if no featured products selected
        self.assertEqual(len(response.context['featured_products']), 4)
