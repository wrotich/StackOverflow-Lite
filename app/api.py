import json
from datetime import datetime

#local imports
from flask import Flask
from flask import request, jsonify, abort
from data import *

def create_app():
    app = Flask(__name__)
        
    @app.route('/api/v1/questions/', methods=['GET'])
    def questions():
        # return all questions
        response = jsonify(data['questions'])
        response.status_code = 200
        return response
    
    @app.route('/api/v1/questions/<questionid>', methods=['GET'])
    def question(id, **kwargs):
        """This function fetches a single question using a unique id"""
        questions = data['questions']
        new_question = {}
        for q in questions:
            if int(q['id']) == int(id):
                new_question = q 
            
        if len(new_question) == 0:
            # question not found
            # return error 404
            abort(404)
        else:
            # return the question
            response.status_code = 200
            return jsonify(new_question)

    
    return app
