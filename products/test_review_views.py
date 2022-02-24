""" Testcases for the products app views. """
from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import UserProfile
from .models import Product, Review


class TestViews(TestCase):
    """ Tests for the views. """
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin', 'admin@email.com', 'adminpassword'
        )

        self.user = User.objects.create_user(
            'john', 'john@email.com', 'johnpassword'
        )

        self.product = Product.objects.create(
            name='Test Product', description='Test description.', price=50.00
        )

        self.profile = UserProfile.objects.get(user=self.user)

        self.review = Review.objects.create(
            product=self.product, user_profile=self.profile, name='Some Name',
            body='Review text.'
        )

    def test_can_add_review(self):
        """ Test that the add review view creates a review. """
        self.client.login(username='john', password='johnpassword')
        response = self.client.post(
            f'/products/add_review/{self.product.id}/',
            {'name': 'Some Name',
             'body': 'A review.'}, follow=True)
        reviews = Review.objects.all()
        self.assertEqual(len(reviews), 2)
        self.assertRedirects(response, f'/products/{self.product.id}/')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message, 'Review successfully added.')

    def test_can_edit_review(self):
        """ Test that a review can be edited in the edit review view. """
        self.client.login(username='john', password='johnpassword')
        response = self.client.post(
            f'/products/edit_review/{self.review.id}/',
            {'name': 'New Name',
             'body': self.review.body}, follow=True)
        self.assertRedirects(response, '/profile/')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message, 'Successfully updated review.')
        updated_review = Review.objects.get(id=self.review.id)
        self.assertEqual(updated_review.name, 'New Name')

    def test_can_delete_review(self):
        """ Test that a review can be deleted. """
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(
            f'/products/delete_review/{self.review.id}/')
        self.assertRedirects(response, '/profile/')
        existing_reviews = Review.objects.filter(id=self.review.id)
        self.assertEqual(len(existing_reviews), 0)

    def test_error_messages_when_review_form_not_valid(self):
        """
        Test add and edit review post views to ensure error
        messages are generated when forms are not valid.
        """
        # Add review
        self.client.login(username='john', password='johnpassword')
        add_response = self.client.post(
            f'/products/add_review/{self.product.id}/',
            {'name': '',
             'body': 'A review.'}, follow=True)
        self.assertRedirects(add_response, f'/products/{self.product.id}/')
        add_message = list(add_response.context.get('messages'))[0]
        self.assertEqual(
            add_message.message,
            'Failed to add review. Please try again.')

        # Edit review
        edit_response = self.client.post(
            f'/products/edit_review/{self.review.id}/',
            {'name': '',
             'body': self.review.body}, follow=True)
        self.assertRedirects(edit_response, '/profile/')
        edit_message = list(edit_response.context.get('messages'))[0]
        self.assertEqual(
            edit_message.message,
            'Failed to update review. Please try again.')
