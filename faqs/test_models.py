""" Testcases for the faqs app models. """
from django.test import TestCase
from .models import FAQ


class TestModels(TestCase):
    """ Tests for the models. """
    def test_faq_string_method_returns_question(self):
        """ Test the FAQ model string method. """
        faq = FAQ.objects.create(
            category='OR', question='Test question?', answer='Test answer')
        self.assertEqual(str(faq), 'Test question?')
