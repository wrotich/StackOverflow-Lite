from flask import Blueprint, request, make_response, jsonify, session
from flask.views import MethodView
from ...models import Answer,Question
from ...helpers import jwt_required

answers_blueprint = Blueprint('answers', __name__)


class AnswersAPIView(MethodView):
    @jwt_required
    def put(self, question_id=None, answer_id=None):
        data = request.get_json(force=True)
        data['question_id'] = question_id
        data['answer_id'] = answer_id
        data['user_id'] = session.get('user_id')

        response = Answer(data).update()
        if response == 200:
            response_object = {
                'status': 'success',
                'message': 'Update successful'
            }
            return make_response(jsonify(response_object)), 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'Please provide correct answer and question id'
            }
        return make_response(jsonify(response_object)), 400

    @jwt_required
    def post(self, question_id=None):
        data = request.get_json(force=True)
        data['question_id'], data['user_id'] = question_id, session.get('user_id')
        response = Answer(data).save()
        if response:
            response_object = {'status': 'success', 'message': response}
            return make_response(jsonify(response_object)), 201
        response_object = {
            'status': 'fail',
            'message': 'Unknown question id. Try a different id.'
        }
        return make_response(jsonify(response_object)), 400


class UpdateAnswerAPIView(MethodView):
    """Marks an answers as accepted"""
    @jwt_required
    def put(self,question_id = None, answer_id = None):
        data = request.get_json(force = True)
        data['question_id'] = question_id
        data['answer_id'] = answer_id
        data['user_id'] = session.get('user_id')

        response = Answer(data).update()
        if response == 200:
            response_object = {
                'status': 'success',
                'message': 'Answer Marked as preferred'
            }
            return make_response(jsonify(response_object)), 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'Please provide correct answer and question id'
            }
        return make_response(jsonify(response_object)), 400
        
class AnswersListAPIView(MethodView):
    """
    List API Resource
    """
    @jwt_required
    def get(self, answer_id=None):
        data = dict()
        data['answer_id'] = answer_id
        data['user_id'] = session.get('user_id')
        if answer_id:
            results = Answer(data).filter_by()
            if len(results) < 1:
                response_object = {
                    'results': 'Answer not found', 'status': 'fail'
                }
                return make_response(jsonify(response_object)), 404
            response_object = {
                'results': results, 'status': 'success'
            }
            return (jsonify(response_object)), 200
        response_object = {'results': Answer(data).query(), 'status': 'success'}
        return (jsonify(response_object)), 200

class ListQuestionAnswersView(MethodView):
    """List all the answers of a specific question"""
    @jwt_required
    def get(self,question_id):
        data = dict()
        data['question_id'] = question_id
        answers = Answer(data).filter_by_question_id()
        print(answers)
        if len(answers) <1:
            response_object = {
                'results': 'No answers posted yet'
            }
            return make_response(jsonify(response_object)),404
        response_object = {
        'results':answers, 'status':'success'
        }
        return (jsonify(response_object)),200
        # response_object = {'results':Answer(data).query(),'status':'success'}
        # return (jsonify(response_object)), 200


# Define the API resources
create_view = AnswersAPIView.as_view('create_api')
create_view1 = UpdateAnswerAPIView.as_view('mark_answer_accepted')
list_view = AnswersListAPIView.as_view('list_api')
list_view1 = ListQuestionAnswersView.as_view('list_api_answers')

# Define the rule for posting an answer
# Add the rule to the blueprint
answers_blueprint.add_url_rule(
    '/api/v1/questions/<string:question_id>/answers',
    view_func=create_view,
    methods=['POST']
)

# Define the rule for updating an answer
# Add the rule to the blueprint
answers_blueprint.add_url_rule(
    '/api/v1/questions/<string:question_id>/answers/<string:answer_id>',
    view_func=create_view,
    methods=['PUT']
    
)
# Define the rule for accepting an answer
# Add the rule to the blueprint
answers_blueprint.add_url_rule(
    '/api/v1/questions/<string:question_id>/answers/<string:answer_id>/accepted',
    view_func=create_view1,
    methods=['PUT']
    
)

# Define the rule for fetching answers
# Add the rule to the blueprint
answers_blueprint.add_url_rule(
    '/api/v1/questions/answers',
    view_func=list_view,
    methods=['GET']
)

# Define the rule for fetching a single answer
# Add the rule to the blueprint
answers_blueprint.add_url_rule(
    '/api/v1/questions/answers/<string:answer_id>',
    view_func=list_view,
    methods=['GET']
)

# Define the rule for fetching answers for a single question
# Add the rule to the blueprint
answers_blueprint.add_url_rule(
    '/api/v1/question/<string:question_id>/answers',
    view_func=list_view1,
    methods=['GET']
)