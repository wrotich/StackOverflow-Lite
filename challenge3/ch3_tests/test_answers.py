import unittest
from flask import Flask
from flask import jsonify, json

class TestAnswer(unittest.TestCase):

    app = Flask(__name__)
    
    def setUp(self):
        self.app.test_client()

    def test_post_answer(self):
        """ Test for posting an answer """
        res2 = self.app.post("/api/v1/questions/1/answer",
            content_type='application/json',
            data=json.dumps(dict(answer="This is my answer 1"),))

        response = json.loads(res2.data)
        self.assertEquals(response["message"], "Answer successfully posted to question")
        self.assertEquals(res2.status_code, 201) 

    def test_post_an_answer_using_wrong_question_id(self):
        res2 = self.app.post("/api/v1/questions/1000/answer",
        content_type='application/json',
        data= json.dumps(dict(answer="This is my answer 1"),))
        response = json.loads(res2.data)
        self.assertEquals(response["message"], "No such question is available")
        self.assertEquals(res2.status_code, 400)

    def test_mark_answer_as_preferred(self):
        pass
    
    def tearDown(self):
        self.app.test_client()