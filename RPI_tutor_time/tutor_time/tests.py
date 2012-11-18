"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from tutor_time.models import *
from settings import CAMPUS_EMAIL_ENDING

class AccountCreationTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        if(self.user_exists('testaccount')):
            user = User.objects.get(username='testaccount')
            Tutee.objects.get(user=user).delete()
            user.delete()

    def user_exists(self, username):
        try:
            User.objects.get(username=username)
        except:
            return False
        return True

    def test_page_load(self):
        """
        Tests that page loads.
        """
        response = self.client.get('/create_account/')
        self.assertEqual(response.status_code, 200)

    def test_create_account_success(self):
        """
        Test to make a real account 
        """
        data = {
            'username': 'testaccount',
            'fname': 'John',
            'lname': 'Doe',
            'email': 'johndoe@'+CAMPUS_EMAIL_ENDING,
            'password': '123456',
            'pwconfirm': '123456',
        }

        response = self.client.post('/create_account/', data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user_exists(data['username']))

    def test_create_account_fail_username1(self):
        """
        Test to make a real account with a number first
        """
        data = {
            'username': '1testaccount',
            'fname': 'John',
            'lname': 'Doe',
            'email': 'johndoe@'+CAMPUS_EMAIL_ENDING,
            'password': '123456',
            'pwconfirm': '123456',
        }

        response = self.client.post('/create_account/', data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user_exists(data['username']))

    def test_create_account_fail_username2(self):
        """
        Test to make a real account with letters after number
        """
        data = {
            'username': 'testaccount1b',
            'fname': 'John',
            'lname': 'Doe',
            'email': 'johndoe@'+CAMPUS_EMAIL_ENDING,
            'password': '123456',
            'pwconfirm': '123456',
        }

        response = self.client.post('/create_account/', data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user_exists(data['username']))

    def test_create_account_fail_username3(self):
        """
        Test to make a real account with no username
        """
        data = {
            'username': '',
            'fname': 'John',
            'lname': 'Doe',
            'email': 'johndoe@'+CAMPUS_EMAIL_ENDING,
            'password': '123456',
            'pwconfirm': '123456',
        }

        response = self.client.post('/create_account/', data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user_exists(data['username']))

    def test_create_account_fail_email1(self):
        """
        Test to make a real account with no email
        """
        data = {
            'username': 'testaccount',
            'fname': 'John',
            'lname': 'Doe',
            'email': '',
            'password': '123456',
            'pwconfirm': '123456',
        }

        response = self.client.post('/create_account/', data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user_exists(data['username']))

    def test_create_account_fail_email2(self):
        """
        Test to make a real account with a email starting with a number
        """
        data = {
            'username': 'testaccount',
            'fname': 'John',
            'lname': 'Doe',
            'email': '1johndoe@'+CAMPUS_EMAIL_ENDING,
            'password': '123456',
            'pwconfirm': '123456',
        }

        response = self.client.post('/create_account/', data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user_exists(data['username']))

    def test_create_account_fail_email3(self):
        """
        Test to make a real account with a email ending with letter after number
        """
        data = {
            'username': 'testaccount',
            'fname': 'John',
            'lname': 'Doe',
            'email': 'johndoe2b@'+CAMPUS_EMAIL_ENDING,
            'password': '123456',
            'pwconfirm': '123456',
        }

        response = self.client.post('/create_account/', data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user_exists(data['username']))

    def test_create_account_fail_email4(self):
        """
        Test to make a real account with a email that's not the email ending 
        """

        # Must not equal the CAMPUS_EMAIL_ENDING
        if CAMPUS_EMAIL_ENDING == 'rpi.edu':
          email = 'rit.edu'
        else:
          email = 'rpi.edu'

        data = {
            'username': 'testaccount',
            'fname': 'John',
            'lname': 'Doe',
            'email': 'johndoe@' + email,
            'password': '123456',
            'pwconfirm': '123456',
        }

        response = self.client.post('/create_account/', data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user_exists(data['username']))

    def test_create_account_fail_email5(self):
        """
        Test to make a real account with a email that's not any edu
        """
        data = {
            'username': 'testaccount',
            'fname': 'John',
            'lname': 'Doe',
            'email': 'johndoe@rpi.com',
            'password': '123456',
            'pwconfirm': '123456',
        }

        response = self.client.post('/create_account/', data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user_exists(data['username']))

    def test_create_account_fail_password1(self):
        """
        Test to make a real account with a short password
        """
        data = {
            'username': 'testaccount',
            'fname': 'John',
            'lname': 'Doe',
            'email': 'johndoe@rpi.com',
            'password': '12345',
            'pwconfirm': '12345',
        }

        response = self.client.post('/create_account/', data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user_exists(data['username']))

    def test_create_account_fail_password2(self):
        """
        Test to make a real account with different passwords
        """
        data = {
            'username': 'testaccount',
            'fname': 'John',
            'lname': 'Doe',
            'email': 'johndoe@rpi.com',
            'password': '123456',
            'pwconfirm': '654321',
        }

        response = self.client.post('/create_account/', data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user_exists(data['username']))

    def test_create_account_fail_firstname1(self):
        """
        Test to make a real account with no first name
        """
        data = {
            'username': 'testaccount',
            'fname': '',
            'lname': 'Doe',
            'email': 'johndoe@rpi.com',
            'password': '123456',
            'pwconfirm': '123456',
        }

        response = self.client.post('/create_account/', data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user_exists(data['username']))

    def test_create_account_fail_lastname1(self):
        """
        Test to make a real account with no last name
        """
        data = {
            'username': 'testaccount',
            'fname': 'John',
            'lname': '',
            'email': 'johndoe@rpi.com',
            'password': '123456',
            'pwconfirm': '123456',
        }

        response = self.client.post('/create_account/', data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user_exists(data['username']))
        
class AccountLoginTest(TestCase):

    def setUp(self):
        """
        Create a user account that can be used for testing authentication.
        """
        User.objects.create_user('testington', 'alpha@'+CAMPUS_EMAIL_ENDING, 'alphabeta')

    def tearDown(self):
        pass

    def not_logged_in(self):
        """
        Make sure no one is initially logged in
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue( "LOGIN" in response.content )

    def log_in(self):
        self.client.login(username='testington', password='alphabeta')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue( 'testington' in response.content )
        
    def log_out(self):
        """Logout testington"""
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue( "LOGIN" in response.content )

    def test_login(self):
        """
        Test login logout flow
        """
        self.not_logged_in()
        self.log_in()
        self.log_out()
