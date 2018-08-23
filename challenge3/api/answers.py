from flask import Flask
from flask import request , jsonify, json
from models import Answer
from db import Database
from datetime import datetime

db_connection = Database()
app = Flask(__name__)
    
@app.route("/api/v2/questions/<question_id>/answers", methods=["POST"])
def add_answer(question_id, user_id):
    db_entries = request.get_json()
    body = db_entries["body"]
    posted_on = datetime.now()

    answer = Answer(body, int(question_id), posted_on,user_id)
    query = 'SELECT question_id FROM questions WHERE question_id=%s;'
    cursor = db_connection.cursor()
    cursor.execute(query, (question_id,))
    row = cursor.fetchall()
    if row:
        cursor.execute(query, (body,))
        answer.save_answer()
        return jsonify({"Message": "Answer added successfully"}), 200

    return jsonify({"message": "Question does not exist"}), 400

# "#@app.route('/api/v2/questions/<question_id>/answers' methods=["PUT"])
# def mark_answer_as_preferred(self):
#     pass"

