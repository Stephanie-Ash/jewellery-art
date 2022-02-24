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

    def test_get_add_product_page(self):
        """ Test the add product page loads. """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get('/products/add/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/add_product.html')

    def test_get_edit_product_page(self):
        """ Test the edit product page loads. """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(f'/products/edit/{self.product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/edit_product.html')

    def test_can_add_product(self):
        """ Test that the add product view creates a product. """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(
            '/products/add/',
            {'name': 'Some Name',
             'description': 'Described.',
             'inventory': 0,
             'price': 10.00}, follow=True)
        product = Product.objects.get(name='Some Name')
        self.assertRedirects(response, f'/products/{product.id}/')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message, 'Successfully added a product to the store.')

    def test_can_edit_product(self):
        """ Test that a product can be edited in the edit product view. """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(
            f'/products/edit/{self.product.id}/',
            {'name': self.product.name,
             'description': self.product.description,
             'inventory': self.product.inventory,
             'price': 5.00}, follow=True)
        self.assertRedirects(response, f'/products/{self.product.id}/')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message, f'Successfully updated {self.product.name}.')
        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.price, 5.00)