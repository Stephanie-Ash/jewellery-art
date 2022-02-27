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
