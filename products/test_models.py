""" Testcases for the products app models. """
from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import UserProfile
from .models import Category, Product, Review


class TestModels(TestCase):
    """ Tests for the models. """
    def setUp(self):
        self.category = Category.objects.create(name='Some Jewellery')
        self.product = Product.objects.create(
            name='Test Product', description='Test description.', price=50.00
        )
        self.user = User.objects.create_user(
            'john', 'john@email.com', 'johnpassword'
        )
        self.profile = UserProfile.objects.get(user=self.user)
        self.review = Review.objects.create(
            product=self.product, user_profile=self.profile, name='Some Name',
            body='Review text.'
        )

    def test_category_string_method_returns_name(self):
        """ Test the Category model string method. """
        self.assertEqual(str(self.category), 'Some Jewellery')

    def test_product_string_method_returns_name(self):
        """ Test the Product model string method. """
        self.assertEqual(str(self.product), 'Test Product')

    def test_review_string_method_includes_name_and_product(self):
        """ Test the Review model string method. """
        self.assertEqual(
            str(self.review), 'Review on Test Product by Some Name')

    def test_category_programmatic_name_generated(self):
        """
        Test that a programmatic name for Category model objects
        is generated on save and that it is the lowercase
        Category name separated by _.
        """
        self.assertEqual(self.category.programmatic_name, 'some_jewellery')

    def test_homepage_featured_defaults_to_false(self):
        """ Test the Product homepage featured field defaults to false. """
        self.assertFalse(self.product.homepage_featured)
