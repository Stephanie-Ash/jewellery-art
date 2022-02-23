""" Testcases for the faqs app forms. """
from django.test import TestCase
from .forms import FAQForm


class TestForms(TestCase):
    """ Tests for the forms. """
    def test_faq_category_is_required(self):
        """ Test that the FAQ category field is required in the form. """
        form = FAQForm({'category': '', 'question': 'Q', 'answer': 'A'})
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors.keys())
        self.assertEqual(form.errors['category'][0], 'This field is required.')

    def test_faq_question_is_required(self):
        """ Test that the FAQ question field is required in the form. """
        form = FAQForm({'category': 'OR', 'question': '', 'answer': 'A'})
        self.assertFalse(form.is_valid())
        self.assertIn('question', form.errors.keys())
        self.assertEqual(form.errors['question'][0], 'This field is required.')

    def test_faq_answer_is_required(self):
        """ Test that the FAQ question field is required in the form. """
        form = FAQForm({'category': 'OR', 'question': 'Q', 'answer': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('answer', form.errors.keys())
        self.assertEqual(form.errors['answer'][0], 'This field is required.')
