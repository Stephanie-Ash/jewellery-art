""" Testcases for the faqs app views. """
from django.test import TestCase
from django.contrib.auth.models import User
from .models import FAQ


class TestViews(TestCase):
    """ Tests for the views. """
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin', 'admin@email.com', 'adminpassword'
        )

        self.user = User.objects.create_user(
            'john', 'john@email.com', 'johnpassword'
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

    def test_superuser_only_areas_redirect_other_users(self):
        """
        Test that views that only allow access by a superuser redirect
        a logged in user to the homepage.
        """
        # Add faq page
        self.client.login(username='john', password='johnpassword')
        add_response = self.client.get('/faqs/add/', follow=True)
        self.assertRedirects(add_response, '/')
        msg_add = list(add_response.context.get('messages'))[0]
        self.assertEqual(
            msg_add.message, 'Sorry this area is for the store owner only.')

        # Edit faq page
        self.client.login(username='john', password='johnpassword')
        edit_response = self.client.get(
            f'/faqs/edit/{self.faq.id}/', follow=True)
        self.assertRedirects(edit_response, '/')
        msg_edit = list(edit_response.context.get('messages'))[0]
        self.assertEqual(
            msg_edit.message, 'Sorry this area is for the store owner only.')

        # Delete faq view
        self.client.login(username='john', password='johnpassword')
        delete_response = self.client.get(
            f'/faqs/delete/{self.faq.id}/', follow=True)
        self.assertRedirects(delete_response, '/')
        msg_delete = list(delete_response.context.get('messages'))[0]
        self.assertEqual(
            msg_delete.message,
            'Sorry, only store owners are authorised to do that.')

    def test_error_messages_when_faq_form_not_valid(self):
        """
        Test add and update faq post views to ensure error message
        is generated when faq form is not valid.
        """
        # Add faq
        self.client.login(username='admin', password='adminpassword')
        add_response = self.client.post(
            '/faqs/add/',
            {
                'category': 'AR',
                'question': 'Test question?',
                'answer': 'Answer'
            }, follow=True)
        add_message = list(add_response.context.get('messages'))[0]
        self.assertEqual(
            add_message.message, 'Failed to add FAQ. Please check the form.')

        # Edit faq
        edit_response = self.client.post(
            f'/faqs/edit/{self.faq.id}/',
            {
                'category': 'AR',
                'question': self.faq.question,
                'answer': self.faq.answer
            }, follow=True)
        edit_message = list(edit_response.context.get('messages'))[0]
        self.assertEqual(
            edit_message.message,
            'Failed to update FAQ. Please check the form.')
