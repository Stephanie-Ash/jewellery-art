""" Testcases for the contact app views. """
from django.test import TestCase


class TestViews(TestCase):
    """ Tests for the views. """
    def test_get_contact_page(self):
        """ Test the contact page loads. """
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')
