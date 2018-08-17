import os
import sys
import unittest
import json

#local imports
from questions import create_app



class QuestionsTests(unittest.TestCase):
    #all the test cases for the questions
    def setUp(self):
        #app initialization"""
        self.client = create_app()
        self.question =  {
            "text":"Which is the best programming laanguage?",
            "year":"2018"
        }
        self.answer =  {
            "text":"You do so by using the int keyword like so: int x;",
            "year":"2018"
        }
        


    def test_get_all_questions(self):
        """Test that a user can obtain all the questions from the API"""
        new_question = self.post_data('/api/v1/questions/', data=self.question)
        self.assertEqual(new_question.status_code, 201)
        res = self.get_data('/api/v1/questions/')
        # check if the correct status code is returned
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.question['text'], str(res.data))

    def test_get_specific_question(self):
        """Test that the API can respond with a particular question, given the id"""
        # post a new question to get a question id in the response
        new_question = self.post_data('/api/v1/questions/', data=self.question)
        self.assertEqual(new_question.status_code, 201)
        response = json.loads(new_question.data.decode('utf-8').replace("'", '"'))
        res = self.get_data('/api/v1/questions/{}'.format(response['id'])) 
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.question['text'], str(res.data))

    def test_post_a_question(self):
        """Test that a user can post a new question"""
        # post a question
        res = self.post_data('/api/v1/questions/', data=self.question)
        self.assertEqual(res.status_code, 201)
        self.assertIn(self.question['text'], str(res.data))

    def test_post_an_answer(self):
        #tests that the user can post an answer to a given question
        new_question = self.post_data('/api/v1/questions/', data=self.question)
        self.assertEqual(new_question.status_code, 201)
        # convert response to JSON
        res = json.loads(new_question.data.decode('utf-8').replace("'", '"'))
        # post an answer to a question
        result = self.post_data('/api/v1/questions/{}/answers'.format(res['id']), data=self.answer)
        self.assertEqual(result.status_code, 201)
        # the response should contain the question id and the answer
        response = json.loads(result.data.decode('utf-8').replace("'", '"'))
        self.assertEqual("{}".format(res['id']), response['question_id'])
        self.assertEqual("{}".format(self.answer['text']), response['text'])


if __name__ == "__main__":
    unittest.main()