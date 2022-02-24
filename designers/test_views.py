""" Testcases for the designers app views. """
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Designer


class TestViews(TestCase):
    """ Tests for the views. """
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin', 'admin@email.com', 'adminpassword'
        )

        self.user = User.objects.create_user(
            'john', 'john@email.com', 'johnpassword'
        )

        self.designer = Designer.objects.create(
            name='Jane Doe', introduction='Test introduction.'
        )

    def test_get_designers_page(self):
        """ Test the designers page loads. """
        response = self.client.get('/designers/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'designers/designers.html')

    def test_get_designer_detail_page(self):
        """ Test the designer detail page loads. """
        response = self.client.get(f'/designers/{self.designer.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'designers/designer_detail.html')

    def test_get_add_desiger_page(self):
        """ Test the add designer page loads. """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get('/designers/add/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'designers/add_designer.html')

    def test_get_edit_designer_page(self):
        """ Test the edit designer page loads. """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(f'/designers/edit/{self.designer.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'designers/edit_designer.html')

    def test_can_add_designer(self):
        """ Test that the add designer view creates a designer. """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(
            '/designers/add/',
            {'name': 'Test', 'introduction': 'Introduced'}, follow=True)
        designer = Designer.objects.get(name='Test')
        self.assertRedirects(response, f'/designers/{designer.id}/')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message, 'Successfully added a designer to the store.')

    def test_can_edit_designer(self):
        """ Test that a designer can be edited in the edit designer view. """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(
            f'/designers/edit/{self.designer.id}/',
            {
                'name': self.designer.name,
                'introduction': 'New introduction'
            }, follow=True)
        self.assertRedirects(response, f'/designers/{self.designer.id}/')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message, f'Successfully updated {self.designer.name}.')
        updated_designer = Designer.objects.get(id=self.designer.id)
        self.assertEqual(updated_designer.introduction, 'New introduction')
