from flask import Blueprint, request, make_response, jsonify

from api import bcrypt, db
from models import User


class UserRegistration(object):
    """
    Class handling User Registration 
    """

    def post(self):
        result = request.get_json()
        user = User.query.filter_by(email=result.get('email')).first()
        if not user:
            try:
                user = User(
                    email=result.get('email'),
                    password=result.get('password')
                )
                db.session.add(user)
                db.session.commit()
                auth_token = user.encode_auth_token(user.id)
                res = {
                    'status': 'success',
                    'message': 'sucess, you are now registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(res)), 201
            except Exception as e:
                res = {
                    'status': 'fail',
                    'message': 'Could not register, try again.'
                }
                return make_response(jsonify(res)), 401
        else:
            res = {
                'status': 'fail',
                'message': 'Already registered. Please Log in.',
            }
            return make_response(jsonify(res)), 202


class UserLogin(object):
    """
    Class enables the User Login 
    """
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': str(user.registered_on)
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401

class UserToken(object):
    """
    User Resource
    """
    def get(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                res = {
                    'status': 'fail',
                    'message': 'wrong token.'
                }
                return make_response(jsonify(res)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                res = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': user.registered_on
                    }
                }
                return make_response(jsonify(res)), 200
            res = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(res)), 401
        else:
            res = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(res)), 401


class LogoutAPI(object):
    """
    Handles user Logout authentication
    """
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            try:
                res = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
                return make_response(jsonify(res)), 200
            except Exception as e:
                res = {
                    'status': 'fail',
                    'message': e
                }
                return make_response(jsonify(res)), 200
            else:
                res = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(res)), 401
        else:
            res = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(res)), 403
