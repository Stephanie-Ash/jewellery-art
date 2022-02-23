""" Testcases for the faqs app views. """
from django.test import TestCase
from django.contrib.auth.models import User
from .models import FAQ


class TestViews(TestCase):
    """ Tests for the views"""
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin', 'admin@email.com', 'adminpassword'
        )

        self.faq = FAQ.objects.create(
            category='OR', question='Test question',
            answer='Test answer'
        )

    def test_get_faq_page(self):
        """ Test the faqs page loads. """
        response = self.client.get('/faqs/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faqs/faqs.html')

    def test_get_add_faq_page(self):
        """ Test the add faq page loads. """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get('/faqs/add/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faqs/add_faq.html')

    def test_get_edit_faq_page(self):
        """ Test the edit faq page loads. """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(f'/faqs/edit/{self.faq.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faqs/edit_faq.html')
