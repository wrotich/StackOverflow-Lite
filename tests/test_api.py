import unittest
from run import app
from flask import jsonify, json
from app.models import Question
from app import api

class TestApi(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_fetch_questions(self):
        '''Test to fetch all questions'''
        res = self.app.post("/api/v1/questions",
            content_type='application/json',
            data=json.dumps(dict(question="This is my question 1"),))
            
        response = json.loads(res.data.decode())
        res2 = self.app.get("/api/v1/questions",
        content_type='application/json',
            data=response)
        response2 = json.loads(res2.data.decode())
        self.assertEquals(response2["message"],"Successfully viewed Questions")
        self.assertEquals(res2.status_code, 200)



    def test_fetch_a_single_question(self):
        '''Test to fetch single question'''
        res = self.app.post("/api/v1/questions",
            content_type='application/json',
            data=json.dumps(dict(question="This is my question 1"),))
        res = self.app.post("/api/v1/questions",
            content_type='application/json',
            data=json.dumps(dict(question="This is my question 2"),))
            
        response = json.loads(res.data.decode())
        res2 = self.app.get("/api/v1/questions/2",
        content_type='application/json',
            data=response)
        response2 = json.loads(res2.data.decode())
        self.assertEquals(response2["message"],"Successfully viewed Question")
        self.assertEquals(res2.status_code, 200)


    def test_post_new_question(self):
        """ Test for posting a new question successfully """
        res = self.app.post("/api/v1/questions",
            content_type='application/json',
            data=json.dumps(dict(question="This is my question 1"),))

        response = json.loads(res.data)
        self.assertEquals(response["message"], "New question successfully posted")
        self.assertEquals(res.status_code, 201)

    def test_post_a_question_with_empty_content(self):
        response = self.app.post("/api/v1/questions",
            content_type='application/json',
            data=json.dumps(dict(question=" "),))
        res = json.loads(response.data)
        self.assertEquals(res["message"], "No input was given")
        self.assertEquals(response.status_code, 400)

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
    
    
    def tearDown(self):
        self.app = app.test_client()


