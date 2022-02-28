""" Testcases for the checkout app models. """
from django.test import TestCase
from products.models import Product
from .models import Order, OrderLineItem


class TestModels(TestCase):
    """ Tests for the models. """
    def setUp(self):
        self.product_one = Product.objects.create(
            name='Test Product One', description='Test description.',
            price=50.00, sku='123test'
        )

        self.product_two = Product.objects.create(
            name='Test Product Two', description='Test description.',
            price=20.00
        )

        self.order = Order.objects.create(
            order_number='test1234', full_name='John Doe',
            email='john@email.com', phone_number='01234567890', country='GB',
            address1='1 Road', town_or_city='Town'
        )

        self.order_two = Order.objects.create(
            full_name='John Doe', email='john@email.com',
            phone_number='01234567890', country='GB',
            address1='1 Road', town_or_city='Town'
        )

        self.order_line_item_one = OrderLineItem.objects.create(
            order=self.order, product=self.product_one, quantity=1
        )

        self.order_line_item_two = OrderLineItem.objects.create(
            order=self.order, product=self.product_two, quantity=1
        )

        self.order_line_item_three = OrderLineItem.objects.create(
            order=self.order_two, product=self.product_two, quantity=1
        )

    def test_order_string_method_returns_order_number(self):
        """ Test the Order model string method. """
        self.assertEqual(str(self.order), 'test1234')

    def test_orderlineitem_string_method_includes_sku_and_order_number(self):
        """ Test the OrderLineItem model string method includes the product
        sku and order number.
        """
        self.assertEqual(
            str(self.order_line_item_one), 'SKU 123test on order test1234')

    def test_order_number_generated(self):
        """
        Test that an order number is generated on save.
        """
        self.assertIsNotNone(self.order_two.order_number)
