import unittest
from .base import BaseTestCase
from ..models import Question

question = Question()


class QuestionModelTestCase(BaseTestCase):

    def test_list_questions_correctly(self):
        '''Tests listing questions correctly.'''
        response = self.client.get(
            '/api/v1/questions/',
            headers={'Authorization': 'JWT ' + self.token}
        )
        assert response.status_code == 200
        assert response.get_json()['status'] == 'success'

    def test_list_questions_unexpectedly(self):
        '''Tests listing questions in an unexpected way
        e.g: trying to list the questions without using the token header.'''
        response = self.client.get(
            '/api/v1/questions/'
        )
        assert response.status_code == 401
        assert response.get_json().get('message') == 'Unauthorized. Please login'


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

    def test_post_question_using_wrong_payload(self):
        '''Test posting a question using wrong payload'''
        data = {
            'title': [],
            'body': {}
        }
        response = self.client.post(
            '/api/v1/questions', json=data,
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
            '/api/v1/questions', json=data,
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['status'], 'success')

    def test_update_question_wrong_input(self):
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