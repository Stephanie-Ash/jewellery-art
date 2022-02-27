""" Testcases for the products app views. """
from django.test import TestCase
from django.contrib.auth.models import User
from designers.models import Designer, Collection
from profiles.models import UserProfile
from checkout.models import Order, OrderLineItem
from .models import Product, Category


class TestViews(TestCase):
    """ Tests for the views. """
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin', 'admin@email.com', 'adminpassword'
        )

        self.user = User.objects.create_user(
            'john', 'john@email.com', 'johnpassword'
        )

        self.profile = UserProfile.objects.get(user=self.user)

        self.designer_one = Designer.objects.create(
            name='Jane Doe', introduction='Test introduction.'
        )

        self.designer_two = Designer.objects.create(
            name='John Doe', introduction='Test introduction two.'
        )

        self.collection_one = Collection.objects.create(
            designer=self.designer_one, name='Collection one'
        )

        self.collection_two = Collection.objects.create(
            designer=self.designer_one, name='Collection two'
        )

        self.category_one = Category.objects.create(
            name='Test Category One'
        )

        self.category_two = Category.objects.create(
            name='Test Category Two'
        )

        self.product_one = Product.objects.create(
            name='Test Product One', description='Test description.',
            price=50.00
        )

        self.product_two = Product.objects.create(
            category=self.category_one, designer=self.designer_one,
            collection=self.collection_one, name='Test Product Two',
            description='Test description.', price=20.00
        )

        self.product_three = Product.objects.create(
            category=self.category_two, designer=self.designer_two,
            collection=self.collection_two, name='Test Product Three',
            description='Test description.', price=10.00
        )

        self.order = Order.objects.create(
            user_profile=self.profile, full_name='John Doe',
            email='john@email.com', phone_number='01234567890', county='GB',
            address1='1 Road', town_or_city='Town'
        )

        self.order_line_item_one = OrderLineItem.objects.create(
            order=self.order, product=self.product_one, quantity=1
        )

        self.order_line_item_two = OrderLineItem.objects.create(
            order=self.order, product=self.product_two, quantity=1
        )

    def test_get_products_page(self):
        """ Test the products page loads. """
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_get_product_detail_page(self):
        """ Test the product detail page loads. """
        response = self.client.get(f'/products/{self.product_one.id}/')
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
        response = self.client.get(f'/products/edit/{self.product_one.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/edit_product.html')

    def test_products_category_filter_displays_correct_products(self):
        """
        Test the products page only displays the products with the selected
        category when the category filter is selected.
        """
        response = self.client.get('/products/?category=test_category_one')
        self.assertIn(self.product_two, response.context['products'])
        self.assertIn(self.category_one, response.context['current_category'])
        self.assertEqual(len(response.context['products']), 1)

    def test_products_designer_filter_displays_correct_products(self):
        """
        Test the products page only displays the products with the selected
        designer when the designer filter is selected.
        """
        response = self.client.get('/products/?designer=jane_doe')
        self.assertIn(self.product_two, response.context['products'])
        self.assertIn(self.designer_one, response.context['current_designer'])
        self.assertEqual(len(response.context['products']), 1)

    def test_products_collection_filter_displays_correct_products(self):
        """
        Test the products page only displays the products with the selected
        collection when the collection filter is selected.
        """
        response = self.client.get('/products/?collection=collection_one')
        self.assertIn(self.product_two, response.context['products'])
        self.assertIn(
            self.collection_one, response.context['current_collection'])
        self.assertEqual(len(response.context['products']), 1)

    def test_products_sort_provides_correct_order(self):
        """
        Test that the products are displayed in the correct order when
        the products page sort option is used.
        """
        self.product_one.category = self.category_two
        self.product_one.designer = self.designer_two
        self.product_one.collection = self.collection_two
        self.product_one.save()

        response_p = self.client.get('/products/?sort=price&direction=desc')
        self.assertEqual(self.product_one, response_p.context['products'][0])

        response_n = self.client.get('/products/?sort=name&direction=asc')
        self.assertEqual(self.product_one, response_n.context['products'][0])

        response_c = self.client.get('/products/?sort=category&direction=asc')
        self.assertEqual(self.product_two, response_c.context['products'][0])

        response_d = self.client.get('/products/?sort=designer&direction=asc')
        self.assertEqual(self.product_two, response_d.context['products'][0])

        response_cn = self.client.get(
            '/products/?sort=collection&direction=asc')
        self.assertEqual(self.product_two, response_cn.context['products'][0])

    def test_products_search_provides_correct_products(self):
        """
        Test that the products page search option filters out the correct
        products.
        """
        response = self.client.get('/products/?q=three')
        self.assertEqual(self.product_three, response.context['products'][0])
        self.assertEqual(len(response.context['products']), 1)

        response_none = self.client.get('/products/?q=', follow=True)
        self.assertRedirects(response_none, '/products/')
        message = list(response_none.context.get('messages'))[0]
        self.assertEqual(message.message, 'Please enter some search criteria!')

    def test_contents_of_product_detail_other_products(self):
        """
        Test that the product detail page other products context only
        contains products by the product designer.
        """
        product = Product.objects.create(
            designer=self.designer_one, name='Extra Product',
            description='Test description.', price=20.00)

        response = self.client.get(f'/products/{self.product_two.id}/')
        self.assertEqual(response.context['other_products'][0], product)
        self.assertEqual(len(response.context['other_products']), 1)

    def test_product_detail_purchased_is_correct_value(self):
        """
        Test that the purchased context of the product detail page us true
        if the user has previously bought the product.
        """
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(f'/products/{self.product_one.id}/')
        self.assertTrue(response.context['purchased'])

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
            f'/products/edit/{self.product_one.id}/',
            {'name': self.product_one.name,
             'description': self.product_one.description,
             'inventory': self.product_one.inventory,
             'price': 5.00}, follow=True)
        self.assertRedirects(response, f'/products/{self.product_one.id}/')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message, f'Successfully updated {self.product_one.name}.')
        updated_product = Product.objects.get(id=self.product_one.id)
        self.assertEqual(updated_product.price, 5.00)

    def test_can_delete_product(self):
        """ Test that a product can be deleted. """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(f'/products/delete/{self.product_one.id}/')
        self.assertRedirects(response, '/products/')
        existing_products = Product.objects.filter(id=self.product_one.id)
        self.assertEqual(len(existing_products), 0)

    def test_can_toggle_homepage_featured(self):
        """
        Test that the toggle homepage featured view changes the value of
        the homepage featured field.
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(
            f'/products/toggle/{self.product_one.id}/')
        self.assertRedirects(response, '/products/')
        updated_product = Product.objects.get(id=self.product_one.id)
        self.assertTrue(updated_product.homepage_featured)

    def test_can_update_inventory(self):
        """
        Test that the update inventory view updates the product inventory.
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(
            f'/products/update_inventory/{self.product_one.id}/',
            {'inventory': 5}, follow=True)
        self.assertRedirects(response, '/products/')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message,
            f'The inventory of {self.product_one.name} has been updated')
        updated_product = Product.objects.get(id=self.product_one.id)
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
            f'/products/edit/{self.product_one.id}/', follow=True)
        self.assertRedirects(edit_response, '/')
        msg_edit = list(edit_response.context.get('messages'))[0]
        self.assertEqual(
            msg_edit.message, 'Sorry this area is for the store owner only.')

        # Delete product view
        self.client.login(username='john', password='johnpassword')
        delete_response = self.client.get(
            f'/products/delete/{self.product_one.id}/', follow=True)
        self.assertRedirects(delete_response, '/')
        msg_delete = list(delete_response.context.get('messages'))[0]
        self.assertEqual(
            msg_delete.message,
            'Sorry, only store owners are authorised to do that.')

        # Update inventory view
        self.client.login(username='john', password='johnpassword')
        update_response = self.client.get(
            f'/products/update_inventory/{self.product_one.id}/', follow=True)
        self.assertRedirects(update_response, '/')
        msg_update = list(update_response.context.get('messages'))[0]
        self.assertEqual(
            msg_update.message, 'Sorry only a store owner can do this.')

        # Toggle homepage featured view
        self.client.login(username='john', password='johnpassword')
        toggle_response = self.client.get(
            f'/products/toggle/{self.product_one.id}/',
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
            f'/products/edit/{self.product_one.id}/',
            {'name': '',
             'description': self.product_one.description,
             'inventory': self.product_one.inventory,
             'price': self.product_one.price}, follow=True)
        edit_message = list(edit_response.context.get('messages'))[0]
        self.assertEqual(
            edit_message.message, f'Failed to update {self.product_one.name}. \
                    Please check the form.')

    def test_error_messages_for_get_update_inventory_view(self):
        """
        Test to ensure redirect and error messages when a get request is
        sent to the update inventory view.
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(
            f'/products/update_inventory/{self.product_one.id}/', follow=True)
        self.assertRedirects(response, '/products/')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message, 'Sorry that action is not possible.')
