from datetime import datetime, timedelta
from api.db import Database
from flask import current_app
import jwt

db_connection = Database()

def create_table(self):
    self.queries = [
        'CREATE TABLE IF NOT EXISTS users (\
                user_id SERIAL PRIMARY KEY,\
                first_name VARCHAR(30),\
                last_name VARCHAR(30),\
                username VARCHAR(30),\
                email VARCHAR(90),\
                password VARCHAR(90)\
                )',
    
        'CREATE TABLE IF NOT EXISTS questions (\
                question_id SERIAL PRIMARY KEY,\
                title VARCHAR(70),\
                content VARCHAR(200),\
                user_id INTEGER REFERENCES users (user_id) ON DELETE CASCADE,\
                posted_date TIMESTAMP)',

        'CREATE TABLE IF NOT EXISTS answers (\
                answer_id SERIAL PRIMARY KEY,\
                answer_body VARCHAR(200),\
                question_id INTEGER REFERENCES questions (question_id) ON DELETE CASCADE,\
                posted_date TIMESTAMP\
                )',
                     
      
        'CREATE TABLE IF NOT EXISTS tokens (\
                token_id SERIAL PRIMARY KEY,\
                token VARCHAR(200)\
                )'
    
    ]
        
    return self.queries


class User(object):

    def __init__(self,first_name,last_name,username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
        
    def save_user(self):
        querry = 'INSERT INTO users (first_name, last_name,username,\
                              email, password) VALUES (%s,%s,%s,%s,%s)'

        cursor = db_connection.cursor()
        cursor.execute(querry,(self.first_name,self.last_name,self.username,\
                               self.email,self.password))
        db_connection.commit()

    @staticmethod
    def token_generator(user_id):

        '''method which generates token for users'''
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=100),
                'iat': datetime.utcnow(),
                'sub': user_id

            }
            token = jwt.encode(
                payload, current_app.config['SECRET_KEY']
            )
            return token

        except Exception as e:
            return e

    @staticmethod  
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

class Tokens():
    def __init__(self, token):
        self.token = token

    @staticmethod
    def verify_token(token):
        '''query db to  check if token exist
        '''
        query = 'SELECT token FROM tokens WHERE token =%s'
        cursor = db_connection.cursor()
        cursor.execute(query, (str(token),))
        blacklisted_token = cursor.fetchone()
        if blacklisted_token:
            return True
        return False

    def save_token(self, token):
        ''' persit token '''
        cursor = db_connection.cursor()
        query = 'INSERT INTO tokens (token) VALUES (%s)'
        cursor.execute(query, (token,))
        db_connection.commit()


