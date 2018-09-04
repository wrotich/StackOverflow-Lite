import unittest
from random import randint
from .base import BaseTestCase


class AuthApiTestCase(BaseTestCase):

    def signup_user(self):
        """This method registers a test user."""
        response = self.client.post('/api/v1/auth/register', json=self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['status'], 'sucess')

    def test_auth_signup_using_wrong_input(self):
        '''Tests signing up using wrong input e.g wrong email address.'''
        response = self.client.post('/api/v1/auth/signup', json=self.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()['status'], 'fail')

    def test_auth_signup_edgecase(self):
        '''Tests signing up using an edgecase input'''
        self.data['email'] = 'email name'
        response = self.client.post('/api/v1/auth/signup', json=self.data)
        self.assertEqual(response.status_code, 401)

    
    def test_login(self):
        '''Tests login using expected input'''
        response = self.client.post('/api/v1/auth/login', json=self.data)
        self.assertEqual(response.status_code, 200)
    
    def test_login_unavailable_user(self):
        '''Tests login using unexpected input'''
        data = self.data
        data['email'] = 'wrong emal'
        response = self.client.post('/api/v1/auth/login', json=data)
        self.assertEqual(response.status_code, 404)

    def test_login_wrong_email(self):
        '''Tests login using unexpected input'''
        data = self.data
        data['email'] = 'wrong emal'
        response = self.client.post('/api/v1/auth/login', json=data)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
