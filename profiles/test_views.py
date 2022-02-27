""" Testcases for the profiles app views. """
from django.test import TestCase
from django.contrib.auth.models import User


class TestViews(TestCase):
    """ Tests for the views. """
    def setUp(self):
        self.user = User.objects.create_user(
            'john', 'john@email.com', 'johnpassword'
        )

    def test_get_profile_page(self):
        """ Test the profile page loads. """
        self.client.login(username='john', password='johnpassword')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
