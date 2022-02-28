""" Testcases for the basket app views. """
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from products.models import Product


class TestViews(TestCase):
    """ Tests for the views. """
    def setUp(self):
        self.client = Client(HTTP_REFERER='/products/')

        self.user = User.objects.create_user(
            'john', 'john@email.com', 'johnpassword'
        )

        self.product_one = Product.objects.create(
            name='Test Product One', description='Test description.',
            price=50.00, inventory=0
        )

        self.product_two = Product.objects.create(
            name='Test Product Two', description='Test description.',
            price=50.00, inventory=2
        )

    def test_get_basket_page(self):
        """ Test the basket page loads. """
        self.client.login(username='john', password='johnpassword')
        session = self.client.session
        session['country'] = 'GB'
        session.save()
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')

    def test_warning_message_on_get_basket_page_if_item_out_of_stock(self):
        """
        Test that an error message is generated when accessing the basket
        page with an out of stock item in the basket.
        """
        session = self.client.session
        session['basket'] = {
            self.product_one.id: 1,
            self.product_two.id: 1,
        }
        session.save()
        response = self.client.get('/basket/')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, f'There are no longer enough of the following item(s) in \
                stock and they have been removed from your basket: \
                    {self.product_one.name}.')

    def test_can_add_to_basket(self):
        """ Test that the add to basket view adds a product to the basket. """
        response = self.client.post(
            f'/basket/add/{self.product_two.id}/',
            {'quantity': 1,
             'redirect_url': f'/products/{self.product_two.id}/'}, follow=True)
        basket = self.client.session['basket']
        self.assertIn(f'{self.product_two.id}', basket.keys())
        self.assertRedirects(response, f'/products/{self.product_two.id}/')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message, f'Added {self.product_two.name} to your basket.')

    def test_can_add_item_already_in_basket_to_basket(self):
        """
        Test that the add to basket view updates the quantity when a product
        already in the basket is added.
        """
        session = self.client.session
        session['basket'] = {
            self.product_two.id: 1,
        }
        session.save()
        response = self.client.post(
            f'/basket/add/{self.product_two.id}/',
            {'quantity': 1,
             'redirect_url': f'/products/{self.product_two.id}/'}, follow=True)
        basket = self.client.session['basket']
        self.assertEqual(basket[f'{self.product_two.id}'], 2)
        self.assertRedirects(response, f'/products/{self.product_two.id}/')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message,
            f'Updated the quantity of {self.product_two.name} in your \
                    basket.')

    def test_error_messages_when_add_item_with_no_stock_to_basket(self):
        """
        Test that error messages are generated when an item with not enough
        stock is added to the basket.
        """
        session = self.client.session
        session['basket'] = {
            self.product_two.id: 2,
        }
        session.save()
        response = self.client.post(
            f'/basket/add/{self.product_two.id}/',
            {'quantity': 1,
             'redirect_url': f'/products/{self.product_two.id}/'}, follow=True)
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message, 'There are not enough in stock to add more of \
                    this item to your basket. Quantity in basket: \
                    2, \
                    Quantity in stock: 2.')

        response = self.client.post(
            f'/basket/add/{self.product_one.id}/',
            {'quantity': 1,
             'redirect_url': f'/products/{self.product_one.id}/'}, follow=True)
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message, f'There are only 0 of {self.product_one.name} \
                    in stock and so not enough to add this item \
                    to your basket.')
