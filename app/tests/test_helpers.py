
import unittest
from app.tests.base import BaseTestCase
from ..helpers import (
    encode_auth_token,
    db_config,
    valid_email,
    validate_user_details
)


class HelpersTestCase(BaseTestCase):

    def test_encode_auth_token(self):
        '''Tests encoding the authentication token.'''
        payload = encode_auth_token(self.user_id)
        self.assertEqual(len(str(payload).split('.')), 3)

    def test_invalid_email(self):
        '''Tests whether a wrong email address can be used.'''
        valid = valid_email('invalid-email')
        self.assertEqual(valid,None)
    

    def test_valid_email(self):
        '''Tests the normal and expected case.'''
        valid = valid_email('winniecherop@gmail.com')
        self.assertIsNotNone(valid)

    def test_user_validation(self):
        """ Tests the validation of user details """
        data = {"email": "", "password": "", "username": ""}
        user = validate_user_details(data)
        assert user.get('email') == 'Invalid email. Please enter a valid email'

if __name__ == '__main__':
    unittest.main()
