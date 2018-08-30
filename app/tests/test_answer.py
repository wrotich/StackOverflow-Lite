import unittest
from .base import BaseTestCase
from ..models import Answer
from ..models import Question

answer = Answer()
question = Question()


class AnswersModelTestCase(BaseTestCase):

    # def test_answer_query_correctly(self):
    #     """ Test fetching all answers using the predefined way"""
    #     query = answer.query()
    #     self.assertIsInstance(query, type([]))

    # def test_filter_edgecase(self):
    #     '''Tests  whether one can fetch an answer using edgecases'''
    #     answer.answer_id = None
    #     query = answer.filter_by()
    #     self.assertEqual(query, [])

    # def test_save_wrong_payload(self):
    #     '''Tests saving an answer after passing a wrong json payload'''
    #     question.title, question.body = "Question title", "question body"
    #     question.user_id = self.user_id
    #     result_payload = question.save()
    #     self.data['question_id'] = result_payload.get('question_id')

    #     answer.question_id = self.data.get('question_id')
    #     answer.answer_body = 'answer body'
    #     answer.user_id = None
    #     query = answer.save()
    #     self.assertEqual(query, None)

    # def test_save(self):
    #     '''Tests saving an answer after passing a correct json payload.'''
    #     question.title, question.body = "Question title", "question body"
    #     question.user_id = self.user_id
    #     result_payload = question.save()
    #     self.data['question_id'] = result_payload.get('question_id')

    #     answer.question_id = self.data.get('question_id')
    #     answer.answer_body = 'answer body'
    #     answer.user_id = self.user_id
    #     query = answer.save()
    #     self.data['answer_id'] = query.get('answer_id')
    #     self.assertEqual(query.get('answer_body'), answer.answer_body)

    # def test_update(self):
    #     '''Tests updating an answer.'''
    #     answer.answer_body = 'Update body'
    #     answer.answer_id = self.data.get('answer_id')
    #     query = answer.update()
    #     self.assertEqual(query, 404)

    # def test_delete(self):
    #     '''Tests deleting an answer.'''
    #     query = answer.delete()
    #     self.assertEqual(query, None)

    # def test_answer_author(self):
    #     '''Tests for the answer_author method in the answer model'''
    #     query = answer.answer_author()
    #     self.assertEqual(query, False)

    # def test_accept(self):
    #     '''Tests for the accept method in the answer model'''
    #     query = answer.update_accept_field()
    #     self.assertEqual(query, True)

    # def test_update_answer(self):
    #     '''Tests for the update_answer method in the answer model'''
    #     query = answer.update_answer()
    #     self.assertEqual(query, True)

    def signup_user(self):
        """This method registers a test user."""
        response = self.client.post('/api/v1/auth/register', json=self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['status'], 'sucess')

    def test_login(self):
        '''Tests login using expected input'''
        response = self.client.post('/api/v1/auth/login', json=self.data)
        self.assertEqual(response.status_code, 200)

    def test_list_answers_unexpected(self):
        '''Tests listing answers incorrectly
        e.g trying to list without JWT authorization header'''
        response = self.client.get(
            '/api/v1/questions/answers'
        )
        self.assertEqual(response.status_code, 401)

    def test_list_answers(self):
        '''Tests listing answers correctly'''
        response = self.client.get(
            '/api/v1/questions/answers',
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'success')

    def test_post_answer(self):
        '''Tests updating an answer'''
        data = {
            'title': 'Test title',
            'body': 'Test body',
            'answer_body': 'Test answer',
            'user': self.user_id
        }

        """ Add test question."""
        self.client.post(
            '/api/v1/questions/', json=data,
            headers={'Authorization': 'JWT ' + self.token}
        )

        response = self.client.get(
            '/api/v1/questions/',
            headers={'Authorization': 'JWT ' + self.token}
        )
        question_id = response.get_json().get('results')[0].get('question_id')

        """ Test posting an answer. """
        response = self.client.post(
            '/api/v1/questions/'+str(question_id)+'/answers', json=data,
            headers={'Authorization': 'JWT ' + self.token}
        )

        self.assertEqual(response.status_code, 201)

        """ Test if a question is created """
        self.assertEqual(response.get_json()['status'], 'success')


if __name__ == '__main__':
    unittest.main()

