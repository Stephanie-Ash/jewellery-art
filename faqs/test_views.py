""" Testcases for the faqs app views. """
from django.test import TestCase
from .models import FAQ


class TestViews(TestCase):
    """ Tests for the views"""

    def test_get_index_page(self):
        """ Test the faqs page loads. """
        FAQ.objects.create(
            category='OR', question='Test question',
            answer='Test answer'
        )
        response = self.client.get('/faqs/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faqs/faqs.html')
