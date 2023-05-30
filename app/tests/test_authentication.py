import unittest
from random import randint
from .base import BaseTestCase


class AuthApiTestCase(BaseTestCase):

    def test_signup_existing_user(self):
        """This method tests registration of an already existing user."""
        response = self.client.post('/api/v1/auth/signup', json=self.data, 
        content_type="application/json")
        self.assertEqual(response.status_code, 401)
        

    def test_auth_signup_wrong_email(self):
        '''Tests signing up using wrong input e.g wrong email address.'''
        response = self.client.post('/api/v1/auth/signup', json=self.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()['status'], 'fail')

    def test_auth_signup_with_blank_email(self):
        '''Tests signing up using an edgecase input'''
        self.data['email'] = 'email name'
        response = self.client.post('/api/v1/auth/signup', json=self.data)
        self.assertEqual(response.status_code, 401)

    
    def test_login(self):
        '''Tests login using expected input'''
        response = self.client.post('/api/v1/auth/login', json=self.data)
        self.assertEqual(response.status_code, 200)
    
    def test_login_unavailable_user(self):
        '''Tests login using unavailable user'''
        data = self.data
        data['email'] = 'wrong email'
        response = self.client.post('/api/v1/auth/login', json=data)
        self.assertEqual(response.status_code, 404)

    def test_login_empty_email(self):
        '''Tests login using empty email input'''
        data = self.data
        data['email'] = 'email'
        response = self.client.post('/api/v1/auth/login', json=data)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
