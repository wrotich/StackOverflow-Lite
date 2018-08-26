import unittest
from .base import BaseTestCase
from ..models import Answer
from ..models import Question

answer = Answer()
question = Question()


class AnswersModelTestCase(BaseTestCase):

    def test_answer_query_normal(self):
        """ Test retrieve all answers"""
        query = answer.query()
        self.assertIsInstance(query, type([]))

    def test_answer_model_filter_edgecase(self):
        """ Example: answer_id '[]' """
        answer.answer_id = None
        query = answer.filter_by()
        self.assertEqual(query, [])

    def test_model_save_unexpected(self):
        """ Pass wrong json payload """
        question.title, question.body = "Question title", "question body"
        question.user_id = self.user_id
        result_payload = question.save()
        self.data['question_id'] = result_payload.get('question_id')

        answer.question_id = self.data.get('question_id')
        answer.answer_body = 'answer body'
        answer.user_id = None
        query = answer.save()
        self.assertEqual(query, None)

    def test_model_save_normal(self):
        question.title, question.body = "Question title", "question body"
        question.user_id = self.user_id
        result_payload = question.save()
        self.data['question_id'] = result_payload.get('question_id')

        answer.question_id = self.data.get('question_id')
        answer.answer_body = 'answer body'
        answer.user_id = self.user_id
        query = answer.save()
        self.data['answer_id'] = query.get('answer_id')
        self.assertEqual(query.get('answer_body'), answer.answer_body)

    def test_model_update(self):
        answer.answer_body = 'Update body'
        answer.answer_id = self.data.get('answer_id')
        query = answer.update()
        self.assertEqual(query, 404)

    def test_model_delete(self):
        query = answer.delete()
        self.assertEqual(query, None)

    def test_model_question_author(self):
        query = answer.question_author()
        self.assertEqual(query, False)

    def test_model_answer_author(self):
        query = answer.answer_author()
        self.assertEqual(query, False)

    def test_model_accept(self):
        query = answer.update_accept_field()
        self.assertEqual(query, True)

    def test_model_update_answer(self):
        query = answer.update_answer()
        self.assertEqual(query, True)

    def test_model_init(self):
        keys = answer.config.keys()
        self.assertIn(list(keys)[0], ['password', 'user', 'database', 'host'])
        self.assertEqual(len(list(keys)), 4)
    def test_list_answers_unexpected(self):
        """ Without JWT authorization header """
        response = self.client.get(
            '/api/v1/questions/answers'
        )
        self.assertEqual(response.status_code, 401)

    def test_list_answers_normal(self):
        """ With JWT authorization"""
        response = self.client.get(
            '/api/v1/questions/answers',
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'success')

    def test_post_update(self):
        data = {
            'title': 'Test title',
            'body': 'Test body',
            'answer_body': 'Test answer',
            'user': self.user_id
        }

        """ Add test question"""
        self.client.post(
            '/api/v1/questions/', json=data,
            headers={'Authorization': 'JWT ' + self.token}
        )

        response = self.client.get(
            '/api/v1/questions/',
            headers={'Authorization': 'JWT ' + self.token}
        )
        question_id = response.get_json().get('results')[0].get('question_id')

        """ Test post answer """
        response = self.client.post(
            '/api/v1/questions/'+str(question_id)+'/answers', json=data,
            headers={'Authorization': 'JWT ' + self.token}
        )

        """ Test status """
        self.assertEqual(response.status_code, 201)

        """ Test if a question is created """
        self.assertEqual(response.get_json()['status'], 'success')


if __name__ == '__main__':
    unittest.main()
