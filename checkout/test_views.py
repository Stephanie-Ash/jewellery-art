""" Testcases for the checkout app views. """
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from products.models import Product
from profiles.models import UserProfile
from .models import Order, OrderLineItem


class TestViews(TestCase):
    """ Tests for the views. """
    def setUp(self):
        self.user = User.objects.create_user(
            'john', 'john@email.com', 'johnpassword'
        )

        self.product_one = Product.objects.create(
            name='Test Product One', description='Test description.',
            price=50.00, inventory=0
        )

        self.product_two = Product.objects.create(
            name='Test Product Two', description='Test description.',
            price=20.00, inventory=2
        )

        self.order = Order.objects.create(
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

    def test_get_login_or_guest_page(self):
        """ Test the login or guest page loads. """
        session = self.client.session
        session['basket'] = {
            self.product_two.id: 1,
        }
        session.save()
        response = self.client.get('/checkout/login_or_guest/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/login_or_guest.html')

    def test_get_checkout_page(self):
        """ Test the checkout page loads. """
        session = self.client.session
        session['basket'] = {
            self.product_two.id: 1,
        }
        session.save()
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

    def test_get_checkout_success_page(self):
        """ Test the checkout success page loads. """
        session = self.client.session
        session['basket'] = {
            self.product_two.id: 1,
        }
        session.save()
        order = self.order
        response = self.client.get(
            f'/checkout/checkout_success/{self.order.order_number}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message, f'Good news, your order was successful. \
        Your order number is: {order.order_number}. A confirmation has been \
        sent to {order.email}')
        # Test the basket is deleted from the session
        session = self.client.session
        self.assertNotIn('basket', session.keys())

    def test_login_or_guest_page_redirects_logged_in_users(self):
        """
        Test the login or guest page redirects logged in users
        to the chekout page.
        """
        self.client.login(username='john', password='johnpassword')
        session = self.client.session
        session['basket'] = {
            self.product_two.id: 1,
        }
        session.save()
        response = self.client.get('/checkout/login_or_guest/')
        self.assertRedirects(response, '/checkout/')

    def test_profile_information_saved_in_checkout_success_view(self):
        """
        Test that the default delivery informaion is saved to the user
        profile when the save info box is ticked.
        """
        self.client.login(username='john', password='johnpassword')
        session = self.client.session
        session['save_info'] = True
        session.save()
        self.client.get(
            f'/checkout/checkout_success/{self.order.order_number}/')
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.default_address1, self.order.address1)

    def test_error_message_generated_by_checkout_when_basket_empty(self):
        """
        Test that the checout view redirects and an error message is genetated
        when navigating there with an empty basket.
        """
        response = self.client.get('/checkout/', follow=True)
        self.assertRedirects(response, '/products/')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message, 'Your basket is currently empty.')

    def test_warning_message_in_checkout_when_basket_item_out_of_stock(self):
        """
        Test that the checkout view redirects and an error message is
        generated when basket items are out of stock.
        """
        session = self.client.session
        session['basket'] = {
            self.product_one.id: 1,
            self.product_two.id: 1
        }
        session.save()
        response = self.client.get('/checkout/', follow=True)
        self.assertRedirects(response, '/checkout/')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message,
            'There are no longer enough of the following item(s) in \
                    stock and they have been removed from your basket: \
                        Test Product One.')

    def test_correct_country_selected_on_checkout_form(self):
        """
        Test that the session country value is displayed on the checkout
        form when available, otherwise GB.
        """
        session = self.client.session
        session['basket'] = {
            self.product_two.id: 1
        }
        session['country'] = ''
        session.save()
        response = self.client.get('/checkout/')
        self.assertEqual(
            response.context['order_form']['country'].value(), 'GB')

        session['country'] = 'US'
        session.save()
        response = self.client.get('/checkout/')
        self.assertEqual(
            response.context['order_form']['country'].value(), 'US')

    def test_correct_country_selected_on_checkout_form_registered_users(self):
        """
        Test that the session country value is displayed on the checkout
        form when available, otherwise the profile default country or GB.
        """
        self.client.login(username='john', password='johnpassword')
        session = self.client.session
        session['basket'] = {
            self.product_two.id: 1
        }
        session['country'] = ''
        session.save()
        response = self.client.get('/checkout/')
        # Value GB when no session variable and no profile default value
        self.assertEqual(
            response.context['order_form']['country'].value(), 'GB')

        session['country'] = ''
        session.save()
        profile = UserProfile.objects.get(user=self.user)
        profile.default_country = 'US'
        profile.save()
        response_2 = self.client.get('/checkout/')
        # Value default profile value when no session variable
        self.assertEqual(
            response_2.context['order_form']['country'].value(), 'US')

        session['country'] = 'AL'
        session.save()
        response_3 = self.client.get('/checkout/')
        # Value session variable even if default profile value available
        self.assertEqual(
            response_3.context['order_form']['country'].value(), 'AL')

        profile.delete()
        response_4 = self.client.get('/checkout/')
        # Value session variable when no profile
        self.assertEqual(
            response_4.context['order_form']['country'].value(), 'AL')

        session['country'] = ''
        session.save()
        response_5 = self.client.get('/checkout/')
        # Value GB when no session variable and no profile
        self.assertEqual(
            response_5.context['order_form']['country'].value(), 'GB')

    def test_can_create_order(self):
        """ Test that the checkout view can create an order. """
        session = self.client.session
        session['basket'] = {
            self.product_two.id: 1
        }
        session['country'] = 'GB'
        session.save()
        response = self.client.post(
            '/checkout/',
            {'full_name': 'Test Name',
             'phone_number': '01234567890',
             'email': 'email@email.com',
             'address1': '1 Road',
             'address2': '',
             'town_or_city': 'Town',
             'county': '',
             'postcode': 'ST1 1AA',
             'client_secret': 'test_secret_test'})
        order = Order.objects.get(full_name='Test Name')
        self.assertRedirects(
            response, f'/checkout/checkout_success/{order.order_number}/')

    def test_update_inventory_view_updates_product_inventory(self):
        """
        Test that the update inventory review updates the product
        inventory and returns a status 200 when the basket products are
        in stock.
        """
        session = self.client.session
        session['basket'] = {
            self.product_two.id: 1
        }
        session.save()
        response = self.client.post('/checkout/update_inventory/')
        self.assertEqual(response.status_code, 200)
        product = Product.objects.get(id=self.product_two.id)
        self.assertEqual(product.inventory, 1)

    def test_update_inventory_error_when_product_out_of_stock(self):
        """
        Test the update inventory view generates an error message and returns
        status 400 when product out of stock
        """
        session = self.client.session
        session['basket'] = {
            self.product_one.id: 1
        }
        session.save()
        response = self.client.post('/checkout/update_inventory/')
        self.assertEqual(response.status_code, 400)
        messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(
            messages[0].message, 'Sorry your payment could not be processed due to \
                out of stock items.')
