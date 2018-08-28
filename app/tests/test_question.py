import unittest
from .base import BaseTestCase
from ..models import Question

question = Question()


class QuestionModelTestCase(BaseTestCase):

    def test_save_question_with_wrong_input(self):
        '''Tests whether a question with wrong input can be saved. '''
        try:
            question.title, question.body, question.user_id = '*', '\\', self.user_id
            question.save()
            assert False
        except AssertionError:
            assert True

    def test_save_question_with_correct_input(self):
        '''Tests whether a question with correct input can be saved. '''
        question.title, question.body = "Question title", "question body"
        question.user_id = self.user_id
        result_payload = question.save()
        self.data['question_id'] = result_payload.get('id')
        self.assertEqual(result_payload.get('body'), question.body)

    def test_filter_by_a_wrong_boundary(self):
        '''Tests Questions model filter_by using a wrong boundary.'''
        question.question_id = None
        result_payload = question.filter_by()
        self.assertEqual(result_payload, None)

    def test_filter_by_correct_input(self):
        '''Tests Questions model filter_by using corrected input. '''
        question.question_id = 1
        result_payload = question.filter_by()
        self.assertEqual(len(list(result_payload.keys())), 2)

    def test_filter_by_edgecase(self):
        '''Tests Questions model filter_by using values that require special handling. '''
        question.question_id = {}
        result_payload = question.filter_by()
        self.assertEqual(result_payload, None)

    def test_filter_user_wrong_boundary(self):
        '''Tests Questions model filter_by using wrong boundary 
        Example: user_id 'None' '''
        question.user_id = None
        query = question.filter_by_user()
        self.assertEqual(query, None)

    def test_filter_user_edgecase(self):
        '''Tests Questions model filter_by using values that require special handling. 
        e.g: user_id '{}' '''
        question.user_id = {}
        query = question.filter_by_user()
        self.assertEqual(query, None)

    def test_filter_user_correct_input(self):
        '''Tests Questions model filter_user using correct/expected input.'''
        question.user_id = self.user_id
        query = question.filter_by_user()
        self.assertEqual(type(query.get('question')), type([]))

    def test_update_wrong_boundary(self):
        '''Tests Questions model update using wrong boundary. 
        e.g: question_id 'None' '''
        question.question_id = None
        query = question.update()
        self.assertEqual(query, True)

    def test_update_edgecase(self):
        '''Tests Questions model update using values that require special handling. 
        e.g: user_id '{}' '''
        question.question_id = ()
        query = question.update()
        self.assertEqual(query, False)

    def test_update_correct_input(self):
        '''Tests Questions model update using correct input.'''
        question.question_id = self.data.get('question_id')
        question.title = 'Hello'
        query = question.update()
        self.assertEqual(query, True)

    def test_delete(self):
        '''Tests Questions model delete.'''
        query = question.delete()
        self.assertEqual(query, False)

    def test_list_questions_unexpectedly(self):
        '''Tests listing questions in an unexpected way
        e.g: trying to list the questions without using the token header.'''
        response = self.client.get(
            '/api/v1/questions/'
        )
        assert response.status_code == 401
        assert response.get_json().get('message') == 'Unauthorized. Please login'

    def test_list_questions_normal(self):
        '''Tests listing questions correctly
        e.g: trying to list the questions without using the token header.'''
        response = self.client.get(
            '/api/v1/questions/',
            headers={'Authorization': 'JWT ' + self.token}
        )
        assert response.status_code == 200
        assert response.get_json()['status'] == 'success'

    def test_fetch_question_using_wrong_input(self):
        '''Tests fetching a question using a wrong input. '''
        response = self.client.get(
            '/api/v1/questions/1str',
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['status'], 'fail')

    def test_fetch_a_question_correct_input(self):
        '''Tests fetching a question using a correct input. '''
        response = self.client.get(
            '/api/v1/questions/1',
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'success')

    def test_fetch_question_edgecase(self):
        '''Tests fetching a question using input that require special handling. 
        e.g: question_id []'''
        response = self.client.get(
            '/api/v1/questions/[]',
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['status'], 'fail')

    def test_post_question_post_wrong_payload(self):
        '''Test posting a question using wrong payload'''
        data = {
            'title': [],
            'body': {}
        }

        response = self.client.post(
            '/api/v1/questions/', json=data,
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['status'], 'fail')

    def test_post_question_correct_input(self):
        '''Test posting a question using correct input'''
        data = {
            'title': 'Test title',
            'body': 'Test body',
            'user': self.user_id
        }

        response = self.client.post(
            '/api/v1/questions/', json=data,
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['status'], 'success')

    def test_update_question_wrong_boundary(self):
        '''Tests updating a question using a wrong input. '''
        data = {
            'user': self.user_id
        }
        response = self.client.put(
            '/api/v1/questions/1909090k', json=data,
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.get_json()['status'], 'fail')

    def test_update_question_correct_input(self):
        '''Tests updating a question using a correct input. '''
        data = {
            'title': 'Test title',
            'body': 'Test body',
            'user': self.user_id
        }

        response = self.client.put(
            '/api/v1/questions/1', json=data,
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['status'], 'success')

    def test_delete_question_unexpectedly(self):
        '''Tests deleting a question using a wrong way e.g unavailable question_id. '''
        response = self.client.delete(
            '/api/v1/questions/None',
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['status'], 'fail')

    def test_delete_question(self):
        '''Tests deleting a question using a predefined way e.g available question_id.'''
        self.test_post_question_correct_input()
        response = self.client.delete(
            '/api/v1/questions/'+str(self.data.get('question_id')),
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['status'], 'fail')

if __name__ == '__main__':
    unittest.main()
