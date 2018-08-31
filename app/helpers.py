from urllib.parse import urlparse
import datetime
import os
import re
from functools import wraps
from flask import request, make_response, jsonify, session
import jwt
from config import BaseConfig
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt


b_crypt = Bcrypt()

def jwt_required(f):
    """ Ensure jwt token is provided and valid."""
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization').split(' ')[-1]
        except Exception as e:
            return make_response(jsonify({"message": 'Unauthorized. Please login'})), 401
        result = decode_auth_token(auth_header)
        try:
            if int(result):
                pass
        except Exception as e:
            return make_response(jsonify({"message": result})), 401
        return f(*args, **kwargs)
    return decorated_function


def encode_auth_token(user_id):
    """ Encodes a payload to generate JWT Token. """
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        'SECRET_KEY'
    )


def decode_auth_token(auth_token):
    """ This function performs the validation of the auth token """
    try:
        payload = jwt.decode(auth_token, 'SECRET_KEY')
        session['user_id'] = str(payload.get('sub'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Token Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def db_config(database_uri=None):
    """ This function gets the postgres db url and returns the database login details """
    load_dotenv()
    if os.environ.get('DATABASE_URL'):
        database_uri = os.environ.get('DATABASE_URL')

    result = urlparse(database_uri)
    config = {
        'database': result.path[1:],
        'user': result.username,
        'password': result.password,
        'host': result.hostname
    }

    if os.environ.get('APP_SETTINGS') == 'TESTING':
        config['database'] = BaseConfig.TEST_DB
    return config


def valid_email(email):
    """  Validate email using regex. """
    return re.match(r'^.+@([?)[a-zA-Z0-9-.])+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$', email)

def valid_username(username):
    """Validate username using regex"""
    return re.match(r'^([a-zA-Z0-9-.])([a-zA-Z]{2,3})$', username)



def validate_user_details(data):
    '''Handles the validation of user details'''
    errors = {}
    if not valid_username(data.get('username')):
        errors['username'] = 'Invalid Username. Please enter a valid username'
    if not valid_email(data.get('email')):
        errors['email'] = 'Invalid email. Please enter a valid email'
    if not data.get('email'):
        errors['password'] = 'Password required'
    if data.get('user'):
        errors['user_exist'] = 'User already exists. Please Log in.'
    return errors


def validate_login(data):
    '''Validates whether a user can login'''
    errors = {}
    return errors