import unittest
from random import randint
from .base import BaseTestCase


class AuthApiTestCase(BaseTestCase):

    def signup_user(self):
        """This method registers a test user."""
        response = self.client.post('/api/v1/auth/register', json=self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['status'], 'sucess')

    def test_auth_signup_unexpected_case(self):
        '''Tests signing up using wrong input e.g wrong email address.'''
        response = self.client.post('/api/v1/auth/signup', json=self.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()['status'], 'fail')

    def test_auth_signup_edgecase(self):
        '''Tests signing up using an edgecase input'''
        self.data['email'] = 'email name'
        response = self.client.post('/api/v1/auth/signup', json=self.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()['status'], 'fail')
    
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
    
    def test_list_users_unexpected_case(self):
        '''Tests listing all the users using unexpected input, e.g not using the JWT token header.'''
        response = self.client.get(
            '/api/v1/auth/users'
        )
        self.assertEqual(response.status_code, 401)

    def test_list_users(self):
        '''Tests listing all the users using correct/expected input'''
        response = self.client.get(
            '/api/v1/auth/users',
            headers={'Authorization': 'JWT '+self.token}
        )
        self.assertEqual(response.status_code, 200)
        assert response.get_json()['status'] == 'success'


    def test_auth_retrieve_user_unexpected_case(self):
        '''Tests retrieving users using unexpected input'''
        response = self.client.get(
            '/api/v1/auth/users/string',
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['status'], 'fail')

    def test_auth_retrieve_user(self):
        '''Tests retrieving users using correct input'''
        response = self.client.get(
            '/api/v1/auth/users/'+self.user_id,
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'success')

    def test_login_unexpected_input(self):
        '''Tests login using unexpected input'''
        data = self.data
        data['email'] = 'wrong emal'
        response = self.client.post('/api/v1/auth/login', json=data)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
