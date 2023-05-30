import unittest
from flask import Flask
from flask import jsonify, json


class TestQuestions(unittest.TestCase):
    app = Flask(__name__)

    def setUp(self):
        self.app.test_client()

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

    def test_delete_question(self):
        res = self.app.get("/api/v1/questions/<qstn_id>",
            content_type='application/json',
            data=json.dumps(dict(question="This is my question 2"),))

        response = json.loads(res.data.decode())
        res2 = self.app.delete("/api/v1/questions/2",
        content_type='application/json',
            data=response)
        response2 = json.loads(res2.data.decode())
        self.assertEquals(response2["message"],"Successfully deleted Question")
        self.assertEquals(res2.status_code, 200)
    
      def tearDown(self):
        self.app.test_client()