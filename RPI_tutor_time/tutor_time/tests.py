"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

class AccountCreationTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_page_load(self):
        """
        Tests that page loads.
        """
        response = self.client.get('/create_account/')
        self.assertEqual(response.status_code, 200)

    def test_create_account_success(self):
        """Not finished"""
        data = {
            'username': 'testaccount',
            'fname': 'John',
            'lname': 'Doe',
            'email': 'johndoe@rpi.edu',
            'password': '123456',
            'pwconfirm': '123456',
        }

        self.client.post('/create_account/', data)
        self.assertEqual(response.status_code, 200)

