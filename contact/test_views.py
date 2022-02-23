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
