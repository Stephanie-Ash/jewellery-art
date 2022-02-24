""" Testcases for the contact app views. """
from django.test import TestCase
from django.contrib.auth.models import User
from .models import ContactMessage


class TestViews(TestCase):
    """ Tests for the views. """
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin', 'admin@email.com', 'adminpassword'
        )

        self.user = User.objects.create_user(
            'john', 'john@email.com', 'johnpassword'
        )

        self.contact_msg = ContactMessage.objects.create(
            topic='OR', first_name='John', last_name='Doe',
            email='email@email.com', message='Test message.'
        )

    def test_get_contact_page(self):
        """ Test the contact page loads. """
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')

    def test_get_manage_contacts_page(self):
        """ Test the add faq page loads. """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get('/contact/manage/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/manage_contacts.html')

    def test_can_add_contact_message(self):
        """ Test that the contact view creates a contact message. """
        response = self.client.post(
            '/contact/',
            {
                'topic': 'OR',
                'first_name': 'Test',
                'last_name': 'Name',
                'email': 'test@test.com',
                'message': 'Some message'
            }, follow=True)
        self.assertRedirects(response, '/')
        contact_message = ContactMessage.objects.get(first_name='Test')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message, f'Thank you for your message. \
                    A summary has been sent to {contact_message.email}. \
                    We will get back to you as soon as we can.')

    def test_can_toggle_responded(self):
        """
        Test that the toggle responded view changes the value of
        the responded field.
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(
            f'/contact/toggle/{self.contact_msg.id}/')
        self.assertRedirects(response, '/contact/manage/')
        updated_msg = ContactMessage.objects.get(id=self.contact_msg.id)
        self.assertTrue(updated_msg.responded)

    def test_error_messages_when_contact_form_not_valid(self):
        """
        Test contact post view to ensure error message
        is generated when contact form is not valid.
        """
        response = self.client.post(
            '/contact/',
            {
                'topic': 'AR',
                'first_name': 'Test',
                'last_name': 'Name',
                'email': 'test@test.com',
                'message': 'Some message'
            }, follow=True)
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message, 'It has not been possible to submit your message. \
                    Please check the form.')

    def test_superuser_only_areas_redirect_other_users(self):
        """
        Test that views that only allow access by a superuser redirect
        a logged in user to the homepage.
        """
        # Manage contacts page
        self.client.login(username='john', password='johnpassword')
        manage_response = self.client.get('/contact/manage/', follow=True)
        self.assertRedirects(manage_response, '/')
        msg_manage = list(manage_response.context.get('messages'))[0]
        self.assertEqual(
            msg_manage.message, 'Sorry this area is for the store owner only.')

        # Toggle responded view
        self.client.login(username='john', password='johnpassword')
        toggle_response = self.client.get(
            f'/contact/toggle/{self.contact_msg.id}/', follow=True)
        self.assertRedirects(toggle_response, '/')
        msg_toggle = list(toggle_response.context.get('messages'))[0]
        self.assertEqual(
            msg_toggle.message,
            'Sorry, only store owners are authorised to do that.')
