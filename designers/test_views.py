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
