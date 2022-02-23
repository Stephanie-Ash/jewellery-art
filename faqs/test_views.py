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

    def test_can_add_faq(self):
        """ Test that the add faq view creates an faq. """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(
            '/faqs/add/',
            {
                'category': 'OR',
                'question': 'Test question?',
                'answer': 'Answer'
            }, follow=True)
        self.assertRedirects(response, '/faqs/')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message, 'Successfully added a FAQ to the FAQs page.')

    def test_can_edit_faq(self):
        """ Test that an faq can be edited in the edit faq view. """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(
            f'/faqs/edit/{self.faq.id}/',
            {
                'category': self.faq.category,
                'question': self.faq.question,
                'answer': 'New answer'
            }, follow=True)
        self.assertRedirects(response, '/faqs/')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message, 'Successfully updated FAQ.')
        updated_faq = FAQ.objects.get(id=self.faq.id)
        self.assertEqual(updated_faq.answer, 'New answer')

    def test_can_delete_faq(self):
        """ Test that an faq can be deleted. """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(f'/faqs/delete/{self.faq.id}/')
        self.assertRedirects(response, '/faqs/')
        existing_faqs = FAQ.objects.filter(id=self.faq.id)
        self.assertEqual(len(existing_faqs), 0)
