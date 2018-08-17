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
        
    
    return app
