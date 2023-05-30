from flask import Blueprint, request, make_response, jsonify, session
from flask.views import MethodView
from ...models import Question
from ...helpers import jwt_required

question_blueprint = Blueprint('questions', __name__)


class CreateQuestionAPI(MethodView):
    """
    Create API Resource
    """
    @jwt_required
    def get(self, question_id):
        response = Question({'question_id': question_id}).filter_by()
        if not response or not response['question']:
            response_object = {
                'results': 'Question Not found'
            }
            return make_response(jsonify(response_object)), 404
        else:
            response_object = {
                'results': response
            }
            return make_response(jsonify(response_object)), 200
            

    @jwt_required
    def post(self):
        # get the post data
        data = request.get_json(force=True)
        data['user_id'] = session.get('user_id')
        row = Question(data).save()
        if row:
            response_object = {
                'results': row
            }
            return make_response(jsonify(response_object)), 201
        else:
            response_object = Question.record_exists
            res = {'message': 'Question already asked'}
            return make_response(jsonify(res)), 401
            
        response_object = {
            'message': 'Could not post the question. Please try again.'
        }
        return make_response(jsonify(response_object)), 400

    """ DELETE QUESTION """
    @jwt_required
    def delete(self, question_id=None):
        data = dict()
        data['user_id'], data['question_id'] = session.get('user_id'), question_id
        response = Question(data).delete()
        if response == 401:
            response_object = {
                'status': 'fail',
                'message': 'Unauthorized, You cannot delete this question!.'
            }
            return make_response(jsonify(response_object)), 401
        if response == 404:
            response_object = {'status': 'fail', 'message': 'Some error occurred. Question Not Found!.'}
            return make_response(jsonify(response_object)), 404
        if response:
            response_object = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(response_object)), 400
        response_object = {
            'status': 'success',
            'message': 'Question deleted successfully'
        }
        return make_response(jsonify(response_object)), 200

        
class QuestionsListAPI(MethodView):
    """ List API Resource """
    @jwt_required
    def get(self):
        data = dict()
        data['user_id'] = session.get('user_id')
        response_object = {
            'results': Question({'q': request.args.get('q')}).query()
        }
        return (jsonify(response_object)), 200

class UserQuestionsAPI(MethodView):
    """ Lists the questions that are posted by a specific user"""
    @jwt_required
    def get(self):
        data = dict()
        data['user_id'] = session.get('user_id')
        response_object = {
            'results': Question(data).filter_by_user()
        }
        return (jsonify(response_object)), 200

class SearchResultAPI(MethodView):
    """List questions according to search"""
    @jwt_required
    def get(self):
        data = dict()
        data['user_id'] = session.get('user_id')
        response_object = {
            'results': Question({'q':request.args.get('q')}).single_query
        }
        return (jsonify(response_object)), 200

# Define the API resources
create_view = CreateQuestionAPI.as_view('create_api')
list_view1 = QuestionsListAPI.as_view('list_api')
list_view2 = SearchResultAPI.as_view('list_result_api')
list_view3 = UserQuestionsAPI.as_view('list_user_questions')

# Define the rule for posting a qestion
# Add the rule to the blueprint
question_blueprint.add_url_rule(
    '/api/v1/questions',
    view_func=create_view,
    methods=['POST']
)
# Define the rule for deleting a qestion
# Add the rule to the blueprint
question_blueprint.add_url_rule(
    '/api/v1/questions/<question_id>',
    view_func=create_view,
    methods=['DELETE']
)

# Define the rule for Getting a single qestion
# Add the rule to the blueprint
question_blueprint.add_url_rule(
    '/api/v1/questions/<question_id>',
    view_func=create_view,
    methods=['GET']
)

# Define the rule for updating a single qestion
# Add the rule to the blueprint
question_blueprint.add_url_rule(
    '/api/v1/questions/<string:question_id>',
    view_func=create_view,
    methods=['PUT']
)
# Define the rule for fetching all qestions
# Add the rule to the blueprint
question_blueprint.add_url_rule(
    '/api/v1/questions/',
    view_func=list_view1,
    methods=['GET']
)

# Define the rule for fetching all questions during search
# Add the rule to the blueprint
question_blueprint.add_url_rule(
    '/api/v1/questions/results/',
    view_func=list_view2,
    methods=['GET']
)

# Define the rule for fetching all user's questions 
# Add the rule to the blueprint
question_blueprint.add_url_rule(
    '/api/v1/questions/user/',
    view_func=list_view3,
    methods=['GET']
)

