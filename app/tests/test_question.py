import unittest
from .base import BaseTestCase
from ..models import Question

question = Question()


class QuestionModelTestCase(BaseTestCase):

    def test_question_model_save_unexpected_input(self):
        try:
            question.title, question.body, question.user_id = '*', '\\', self.user_id
            question.save()
            assert False
        except AssertionError:
            assert True

    def test_question_model_save_expected_input(self):
        question.title, question.body = "Question title", "question body"
        question.user_id = self.user_id
        result_payload = question.save()
        self.data['question_id'] = result_payload.get('id')
        self.assertEqual(result_payload.get('body'), question.body)

    def test_model_question_filter_by_unexpected_boundary(self):
        question.question_id = None
        result_payload = question.filter_by()
        self.assertEqual(result_payload, None)

    def test_model_question_filter_by_expected_input(self):
        """
            Example: question id 1
        """
        question.question_id = 1
        result_payload = question.filter_by()
        self.assertEqual(len(list(result_payload.keys())), 2)

    def test_model_question_filter_by_unexpected_edgecase(self):
        """
            Example: question id {}, []
        """
        question.question_id = {}
        result_payload = question.filter_by()
        self.assertEqual(result_payload, None)

    def test_question_model_filter_user_unexpected_boundary(self):
        """ Example: user_id 'None' """
        question.user_id = None
        query = question.filter_by_user()
        self.assertEqual(query, None)

    def test_question_model_filter_user_unexpected_edge(self):
        """ Example: user_id '{}' """
        question.user_id = {}
        query = question.filter_by_user()
        self.assertEqual(query, None)

    def test_question_model_filter_user_expected(self):
        question.user_id = self.user_id
        query = question.filter_by_user()
        self.assertEqual(type(query.get('question')), type([]))

    def test_question_model_update_unexpected_boundary(self):
        """ Example: question_id 'None' """
        question.question_id = None
        query = question.update()
        self.assertEqual(query, True)

    def test_question_model_update_unexpected_edge(self):
        """ Example: question_id '()', '{}', '[]' """
        question.question_id = ()
        query = question.update()
        self.assertEqual(query, False)

    def test_question_model_update_normal(self):
        question.question_id = self.data.get('question_id')
        question.title = 'Hello'
        query = question.update()
        self.assertEqual(query, True)

    def test_question_model_delete_normal(self):
        query = question.delete()
        self.assertEqual(query, False)

    def test_question_model_init(self):
        keys = question.config.keys()
        self.assertIn(list(keys)[0], ['password', 'user', 'database', 'host'])
        self.assertEqual(len(list(keys)), 4)
    def test_list_questions_unexpected(self):
        """ Example: Without JWT  token header """
        response = self.client.get(
            '/api/v1/questions/'
        )
        assert response.status_code == 401
        assert response.get_json().get('message') == 'Unauthorized. Please login'

    def test_list_questions_normal(self):
        """ Example: with JWT authorization header """
        response = self.client.get(
            '/api/v1/questions/',
            headers={'Authorization': 'JWT ' + self.token}
        )
        assert response.status_code == 200
        assert response.get_json()['status'] == 'success'

    def test_retrieve_question_unexpected_boundary(self):
        """ Example: question id 'non-numeric' """
        response = self.client.get(
            '/api/v1/questions/1str',
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['status'], 'fail')

    def test_retrieve_question_normal(self):
        """ Example: question_id '1' """
        response = self.client.get(
            '/api/v1/questions/1',
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'success')

    def test_retrieve_question_unexpected_edgecase(self):
        """ Example: question_id [] """
        response = self.client.get(
            '/api/v1/questions/[]',
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['status'], 'fail')

    def test_post_question_unexpected(self):
        """ Example: Send unexpected paylaod """
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

    def test_post_question_normal(self):
        """ Example: Send Expected paylaod """
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

    def test_update_question_unexpected_boundary(self):
        """ Example: Send unexpected paylaod """
        data = {
            'user': self.user_id
        }

        response = self.client.put(
            '/api/v1/questions/1909090k', json=data,
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['status'], 'fail')

    def test_update_question_normal(self):
        """ Example: Send Expected paylaod """
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

    def test_delete_question_unexpected(self):
        """ Example: undefined question_id """
        response = self.client.delete(
            '/api/v1/questions/None',
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['status'], 'fail')

    def test_delete_question_normal(self):
        """ Example: Send Expected paylaod """
        self.test_post_question_normal()
        response = self.client.delete(
            '/api/v1/questions/'+str(self.data.get('question_id')),
            headers={'Authorization': 'JWT ' + self.token}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['status'], 'fail')

if __name__ == '__main__':
    unittest.main()
