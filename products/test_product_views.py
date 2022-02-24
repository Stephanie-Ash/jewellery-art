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

    def test_can_delete_product(self):
        """ Test that a product can be deleted. """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(f'/products/delete/{self.product.id}/')
        self.assertRedirects(response, '/products/')
        existing_products = Product.objects.filter(id=self.product.id)
        self.assertEqual(len(existing_products), 0)

    def test_can_toggle_homepage_featured(self):
        """
        Test that the toggle homepage featured view changes the value of
        the homepage featured field.
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(
            f'/products/toggle/{self.product.id}/')
        self.assertRedirects(response, '/products/')
        updated_product = Product.objects.get(id=self.product.id)
        self.assertTrue(updated_product.homepage_featured)

    def test_can_update_inventory(self):
        """
        Test that the update inventory view updates the product inventory.
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(
            f'/products/update_inventory/{self.product.id}/',
            {'inventory': 5}, follow=True)
        self.assertRedirects(response, '/products/')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message,
            f'The inventory of {self.product.name} has been updated')
        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.inventory, 5)

    def test_superuser_only_areas_redirect_other_users(self):
        """
        Test that views that only allow access by a superuser redirect
        a logged in user to the homepage.
        """
        # Add product page
        self.client.login(username='john', password='johnpassword')
        add_response = self.client.get('/products/add/', follow=True)
        self.assertRedirects(add_response, '/')
        msg_add = list(add_response.context.get('messages'))[0]
        self.assertEqual(
            msg_add.message, 'Sorry this area is for the store owner only.')

        # Edit product page
        self.client.login(username='john', password='johnpassword')
        edit_response = self.client.get(
            f'/products/edit/{self.product.id}/', follow=True)
        self.assertRedirects(edit_response, '/')
        msg_edit = list(edit_response.context.get('messages'))[0]
        self.assertEqual(
            msg_edit.message, 'Sorry this area is for the store owner only.')

        # Delete product view
        self.client.login(username='john', password='johnpassword')
        delete_response = self.client.get(
            f'/products/delete/{self.product.id}/', follow=True)
        self.assertRedirects(delete_response, '/')
        msg_delete = list(delete_response.context.get('messages'))[0]
        self.assertEqual(
            msg_delete.message,
            'Sorry, only store owners are authorised to do that.')

        # Update inventory view
        self.client.login(username='john', password='johnpassword')
        update_response = self.client.get(
            f'/products/update_inventory/{self.product.id}/', follow=True)
        self.assertRedirects(update_response, '/')
        msg_update = list(update_response.context.get('messages'))[0]
        self.assertEqual(
            msg_update.message, 'Sorry only a store owner can do this.')

        # Toggle homepage featured view
        self.client.login(username='john', password='johnpassword')
        toggle_response = self.client.get(
            f'/products/toggle/{self.product.id}/',
            follow=True)
        self.assertRedirects(toggle_response, '/')
        msg_toggle = list(toggle_response.context.get('messages'))[0]
        self.assertEqual(
            msg_toggle.message,
            'Sorry, only store owners are authorised to do that.')

    def test_error_messages_when_product_form_not_valid(self):
        """
        Test add and edit product post views to ensure error
        messages are generated when forms are not valid.
        """
        # Add designer
        self.client.login(username='admin', password='adminpassword')
        add_response = self.client.post(
            '/products/add/',
            {'name': '',
             'description': 'Described.',
             'inventory': 0,
             'price': 10.00}, follow=True)
        add_message = list(add_response.context.get('messages'))[0]
        self.assertEqual(
            add_message.message,
            'Failed to add product. Please check the form.')

        # Edit product
        edit_response = self.client.post(
            f'/products/edit/{self.product.id}/',
            {'name': '',
             'description': self.product.description,
             'inventory': self.product.inventory,
             'price': self.product.price}, follow=True)
        edit_message = list(edit_response.context.get('messages'))[0]
        self.assertEqual(
            edit_message.message, f'Failed to update {self.product.name}. \
                    Please check the form.')

    def test_error_messages_for_get_update_inventory_view(self):
        """
        Test to ensure redirect and error messages when a get request is
        sent to the update inventory view.
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(
            f'/products/update_inventory/{self.product.id}/', follow=True)
        self.assertRedirects(response, '/products/')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message, 'Sorry that action is not possible.')
