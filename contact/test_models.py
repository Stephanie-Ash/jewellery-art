""" Testcases for the contact app models. """
from django.test import TestCase
from .models import ContactMessage


class TestModels(TestCase):
    """ Tests for the models. """
    def test_contact_message_string_method_includes_names(self):
        """ Test the ContactMessage model string method. """
        contact_msg = ContactMessage.objects.create(
            topic='OR', first_name='John', last_name='Doe',
            email='email@email.com', message='Test message.')
        self.assertEqual(str(contact_msg), 'Message from John Doe')

    def test_responded_defaults_to_false(self):
        """ Test the ContactMessage responded field defaults to false. """
        contact_msg = ContactMessage.objects.create(
            topic='OR', first_name='John', last_name='Doe',
            email='email@email.com', message='Test message.')
        self.assertFalse(contact_msg.responded)
