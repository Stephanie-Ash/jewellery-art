""" Testcases for the profile app models. """
from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import UserProfile


class TestModels(TestCase):
    """ Tests for the models. """
    def test_user_profile_string_method_returns_username(self):
        """ Test the UserProfile model string method. """
        test_user = User.objects.create_user(
            'john', 'john@email.com', 'johnpassword'
        )
        test_profile = UserProfile.objects.get(user=test_user)
        self.assertEqual(str(test_profile), 'john')
