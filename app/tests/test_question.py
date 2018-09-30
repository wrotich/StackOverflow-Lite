import unittest
from .base import BaseTestCase
from ..models import Question

question = Question()


class QuestionModelTestCase(BaseTestCase):

    def test_list_questions(self):
        '''Tests listing questions correctly.'''
        response = self.client.get(
            '/api/v1/questions/',
            headers={'Authorization': 'JWT ' + self.token}
        )
        assert response.status_code == 200

    def test_list_questions_using_wrong_token(self):
        '''Tests listing questions in an unexpected way
        e.g: trying to list the questions without using the token header.'''
        response = self.client.get(
            '/api/v1/questions/'
        )
        assert response.status_code == 401
        assert response.get_json().get('message') == 'Unauthorized. Please login'


    def test_fetch_question_using_unavailable_id(self):
        '''Tests fetching a question using a wrong input. '''
        response = self.client.get(
            '/api/v1/questions/1str',
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 404)
    

    def test_fetch_a_question_correct_id(self):
        '''Tests fetching a question using a correct input. '''
        response = self.client.get(
            '/api/v1/questions/917',
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 200)


    def test_fetch_question_with_blank_id(self):
        '''Tests fetching a question using input that require special handling. 
        e.g: question_id []'''
        response = self.client.get(
            '/api/v1/questions/[]',
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 404)
        

    def test_post_question_without_title(self):
        '''Test posting a question using wrong input'''
        data = {
            'title': [],
            'body': {}
        }
        response = self.client.post(
            '/api/v1/questions', json=data,
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 401)


    def test_post_question(self):
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
        


    def test_delete_question_using_wrong_question_id(self):
        '''Tests deleting a question using a wrong way e.g no question_id. '''
        response = self.client.delete(
            '/api/v1/questions/None',
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 400)


    def test_delete_question(self):
        '''Tests deleting a question using a predefined way e.g available question_id.'''
        self.test_post_question()
        question_id = self.data.get('question_id')
        response = self.client.delete(
            '/api/v1/questions/'+str(question_id),
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()