""" Testcases for the profiles app views. """
from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product
from checkout.models import Order, OrderLineItem
from .models import UserProfile


class TestViews(TestCase):
    """ Tests for the views. """
    def setUp(self):
        self.user = User.objects.create_user(
            'john', 'john@email.com', 'johnpassword'
        )

        self.profile = UserProfile.objects.get(user=self.user)

        self.product_one = Product.objects.create(
            name='Test Product One', description='Test description.',
            price=50.00
        )

        self.product_two = Product.objects.create(
            name='Test Product Two', description='Other description.',
            price=20.00
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

    def test_get_profile_page(self):
        """ Test the profile page loads. """
        self.client.login(username='john', password='johnpassword')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_order_history_page(self):
        """ Test the order history page loads. """
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(
            f'/profile/order_history/{self.order.order_number}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
