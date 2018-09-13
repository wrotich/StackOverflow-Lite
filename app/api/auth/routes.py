from flask import Blueprint, request, make_response, jsonify, session
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from ...models import User, Tokens
from ...helpers import jwt_required, encode_auth_token, decode_auth_token,validate_user_details

b_crypt = Bcrypt()
auth_blueprint = Blueprint('auth', __name__)


class RegisterAPI(MethodView):
    """ User Signup API Resource """
    def post(self):
        # get the post data
        data = request.get_json(force=True)
        data['user_id'] = session.get('user_id')
        data['user'] = User(data).filter_by_email()
        # check if user already exists
        errors = validate_user_details(data)
        user = User(data).save()
        if len(errors) < 0:
            user = User(data).save()
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
                'id': user.get('user_id')
            }
            return make_response(jsonify(response_object)), 201
        response_object = {
            'status': 'fail', 'errors': errors
        }
        return make_response(jsonify(response_object)), 401
    


class LoginAPI(MethodView):
    """ User Login API Resource """
    def post(self):
        data = request.get_json(force=True)
        data['user_id'] = session.get('user_id')
        try:
            user = User(data).filter_by_email()
            if len(user) >= 1 and data.get('password'):
                if b_crypt.check_password_hash(user[0].get('password'), data.get('password')):
                    auth_token = encode_auth_token(user[0].get('user_id'))
                else:
                    response_object = {'status': 'fail', 'message': 'Password or email do not match.'}
                    return make_response(jsonify(response_object)), 401
                try:
                    if auth_token:
                        response_object = {
                            'status': 'success', 'id': user[0].get('user_id'),
                            'message': 'Successfully logged in.',
                            'auth_token': auth_token.decode()
                        }
                        return make_response(jsonify(response_object)), 200
                except Exception as e:
                    return {"message": 'Error decoding token'}, 401
            else:
                response_object = {'status': 'fail', 'message': 'User does not exist.'}
                return make_response(jsonify(response_object)), 404
        except Exception as e:
            response_object = {'status': 'fail', 'message': 'Try again'}
            return make_response(jsonify(response_object)), 500


class LogoutAPI(MethodView):
    """
    Handles user Logout authentication
    """
    def post(self):
        # get auth token

        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[0]
        else:
            auth_token = ''
        if auth_token:
            # resp = decode_auth_token(auth_token)
            token = Tokens.__call__(auth_token)
            token.save_auth_header()
            res = {
                'message': 'Successfully logged out.'
            }
            return make_response(jsonify(res)), 200
        res = {
                'message': 'You are logged out, login again'
            }



# Define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
logout_view = LogoutAPI.as_view('logout_api')

# Define the rule for sign up
# Add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/api/v1/auth/signup',
    view_func=registration_view,
    methods=['POST']
)

# Define the rule for deleting a user
# Add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/api/v1/auth/delete',
    view_func=registration_view,
    methods=['DELETE']
)

# Define the rule for login
# Add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/api/v1/auth/login',
    view_func=login_view,
    methods=['POST']
)

# Define the rule for logout
# Add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/api/v1/auth/logout',
    view_func=logout_view,
    methods=['POST']
)
