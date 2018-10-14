from flask import Blueprint, jsonify, session
from flask.views import MethodView
from ...models import Question
from ...models import User
from ...helpers import jwt_required

users_blueprint = Blueprint('users', __name__)


class UsersListAPIView(MethodView):
    """lists a specific user's questions """
    @jwt_required
    def get(self):
        data = {'user_id': session.get('user_id')}
        response_object = {
            'results': Question(data).filter_by_user(),
            'status': 'success'
        }
        return (jsonify(response_object)), 200

class UsersDetailsList(MethodView):
    """Lists all the details of a user"""
    @jwt_required
    def get(self):
        data = {'user_id':session.get('user_id')}
        response_object = {
            'results':User(data).filter_by(),
            'status':'success'
        }
        return (jsonify(response_object)), 200

# Define the API resource
comment_view = UsersListAPIView.as_view('user_api')
list_view = UsersDetailsList.as_view('details_api')

# Define the rule for fetching a single user's questions
# Add the rule to the blueprint
users_blueprint.add_url_rule(
    '/api/v1/users/questions',
    view_func=comment_view,
    methods=['GET']
)

# Define the rule for fetching users details
# Add the rule to the blueprint
users_blueprint.add_url_rule(
    '/api/v1/users/details',
    view_func=list_view,
    methods=['GET']
)
