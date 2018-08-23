from flask import Flask
from flask import request , jsonify, json
from db import Database  
from models import Question
from datetime import datetime

db_connection = Database()
app = Flask(__name__)

@app.route("/api/v2/questions", methods=["GET"])
# fetching all questions
def fetch_questions(self):
    query ='SELECT * FROM questions'
    cursor = db_connection.cursor()
    cursor.execute(query)
    row = cursor.fetchall()
    if len(row) is not 0:
        return jsonify({"Questions": row}), 200
    return jsonify({"Questions": "There are no questions found"}), 404

@app.route("/api/v2/questions/<question_id>", methods=["GET"])
# fetching a single question
def fetch_a_single_question(question_id):
    query = 'SELECT * FROM questions WHERE question_id=%s;'
    cursor = db_connection.cursor()
    cursor.execute(query, (question_id,))
    row = cursor.fetchone()
    if row:
        return jsonify({"Question": row}), 200
    return jsonify({"Questions": "Not question found"}), 404

@app.route("/api/v2/questions", methods=["POST"])
# posting a single question
def post_question(user_id=1):
    db_entries = request.get_json()
    title = db_entries["title"]
    content = db_entries["content"]
    posted_on = datetime.now()
    
    question = Question(user_id,title,content,posted_on)
    query = 'SELECT title FROM questions WHERE title=%s'
    cursor = db_connection.cursor()
    cursor.execute(query, (title,))
    row = cursor.fetchone()
    if not row:
        question.save_question()
        return jsonify({'Message': 'Question has been successfully posted'}), 200
    return jsonify({"message": "Question already asked"}), 409

db_connection.create_tables()

@app.route("/api/v2/questions", methods=["DELETE"])
# delete a question
def delete_a_question(question_id):
    query = 'DELETE row FROM questions WHERE question_id=%s;'
    cursor = db_connection.cursor()
    cursor.execute(query, (question_id,))
    row = cursor.fetchone()
    if row:
        return jsonify({"Question":"Successflully deleted question"}), 200
    return jsonify({"Questions": "No question found"}), 404
    