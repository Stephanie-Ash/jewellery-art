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

    def test_can_delete_designer(self):
        """ Test that a designer can be deleted. """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(f'/designers/delete/{self.designer.id}/')
        self.assertRedirects(response, '/designers/')
        existing_designers = Designer.objects.filter(id=self.designer.id)
        self.assertEqual(len(existing_designers), 0)

    def test_superuser_only_areas_redirect_other_users(self):
        """
        Test that views that only allow access by a superuser redirect
        a logged in user to the homepage.
        """
        # Add designer page
        self.client.login(username='john', password='johnpassword')
        add_response = self.client.get('/designers/add/', follow=True)
        self.assertRedirects(add_response, '/')
        msg_add = list(add_response.context.get('messages'))[0]
        self.assertEqual(
            msg_add.message, 'Sorry this area is for the store owner only.')

        # Edit designer page
        self.client.login(username='john', password='johnpassword')
        edit_response = self.client.get(
            f'/designers/edit/{self.designer.id}/', follow=True)
        self.assertRedirects(edit_response, '/')
        msg_edit = list(edit_response.context.get('messages'))[0]
        self.assertEqual(
            msg_edit.message, 'Sorry this area is for the store owner only.')

        # Delete designer view
        self.client.login(username='john', password='johnpassword')
        delete_response = self.client.get(
            f'/designers/delete/{self.designer.id}/', follow=True)
        self.assertRedirects(delete_response, '/')
        msg_delete = list(delete_response.context.get('messages'))[0]
        self.assertEqual(
            msg_delete.message,
            'Sorry, only store owners are authorised to do that.')

    def test_error_messages_when_designer_form_not_valid(self):
        """
        Test add and update designer post views to ensure error message
        is generated when designer form is not valid.
        """
        # Add designer
        self.client.login(username='admin', password='adminpassword')
        add_response = self.client.post(
            '/designers/add/',
            {'name': '', 'introduction': 'Some words'}, follow=True)
        add_message = list(add_response.context.get('messages'))[0]
        self.assertEqual(
            add_message.message,
            'Failed to add designer. Please check the form.')

        # Edit designer
        edit_response = self.client.post(
            f'/designers/edit/{self.designer.id}/',
            {'name': self.designer.name, 'introduction': ''}, follow=True)
        edit_message = list(edit_response.context.get('messages'))[0]
        self.assertEqual(
            edit_message.message, f'Failed to update {self.designer.name}. \
                    Please check the form.')
