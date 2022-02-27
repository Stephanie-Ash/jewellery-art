""" Testcases for the basket app views. """
from django.test import TestCase


class TestViews(TestCase):
    """ Tests for the views. """
    def test_get_basket_page(self):
        """ Test the basket page loads. """
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
