""" Testcases for the products app views. """
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product


class TestViews(TestCase):
    """ Tests for the views. """
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin', 'admin@email.com', 'adminpassword'
        )

        self.user = User.objects.create_user(
            'john', 'john@email.com', 'johnpassword'
        )

        self.product = Product.objects.create(
            name='Test Product', description='Test description.', price=50.00
        )

    def test_get_products_page(self):
        """ Test the products page loads. """
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_get_product_detail_page(self):
        """ Test the product detail page loads. """
        response = self.client.get(f'/products/{self.product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
