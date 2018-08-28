import psycopg2
import psycopg2.extensions
from psycopg2.extras import RealDictCursor
from .helpers import db_config
from flask_bcrypt import Bcrypt

class Answer:
    def __init__(self, data={}):
        self.config = db_config()
        self.table = 'answers'
        self.answer_body = data.get('answer_body')
        self.question_id = data.get('question_id')
        self.answer_id = data.get('answer_id')
        self.accepted = data.get('accepted')
        self.user_id = data.get('user_id')

    def save(self):
        """
        Creates an answer record in answers table
        :return: None of inserted record
        """
        con, response = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            query = "INSERT INTO answers (user_id, answer_body, question_id) VALUES (%s, %s, %s) RETURNING *; "
            cur.execute(query, (self.user_id, self.answer_body, self.question_id))
            con.commit()
            response = cur.fetchone()
        except Exception as e:
            con.close()
        con.close()
        return response

    def query(self):
        """
        Fetch all records from a answers table
        :return: list: query set
        """
        con = psycopg2.connect(**self.config)
        cur = con.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """ SELECT * FROM  answers
            """
        )
        queryset_list = cur.fetchall()
        con.close()
        return queryset_list

    def filter_by(self):
        """
        Select a column(s) from answer table
        :return: list: queryset list
        """
        try:
            con = psycopg2.connect(**self.config)
            cur = con.cursor(cursor_factory=RealDictCursor)
            query = "SELECT * FROM answers WHERE answer_id={}"
            cur.execute(query.format(self.answer_id))
            queryset_list = cur.fetchall()
            con.close()
            return queryset_list
        except Exception as e:
            con.close()
            return []

    def question_author(self):
        con = psycopg2.connect(**self.config)
        cur = con.cursor(cursor_factory=RealDictCursor)
        query = "SELECT user_id FROM questions WHERE question_id=%s"
        cur.execute(query, self.question_id)
        return cur.fetchall()
        con.close()
        return False

    def answer_author(self):
        try:
            con = psycopg2.connect(**self.config)
            cur = con.cursor(cursor_factory=RealDictCursor)
            query = "SELECT user_id FROM answers WHERE answer_id=%s"
            cur.execute(query, self.answer_id)
            queryset_list = cur.fetchall()
            con.close()
            return queryset_list
        except Exception as e:
            return False

    def update(self):
        try:
            answer_author = self.answer_author()[0].get('user_id')
            question_author = self.question_author()[0].get('user_id')
            # current user is the answer author
            if int(answer_author) == int(self.user_id):
                # update answer
                response = 200 if self.update_answer() else 304
                return response

            # current user is question author
            elif int(question_author) == int(self.user_id):
                # mark it as accepted
                response = self.update_accept_field()
                response = 200 if response else 304
                return response
            # other users
            else:
                return 203
        except:
            return 404

    def update_accept_field(self):
        """
        Update an answer column
        :return: bool:
        """
        con, result = psycopg2.connect(**self.config), True
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            query = "UPDATE answers SET accepted=%s WHERE answer_id=%s AND question_id=%s"
            cur.execute(query, (self.accepted, self.answer_id, self.question_id))
            con.commit()
        except Exception as e:
            result = False
        con.close()
        return result

    def update_answer(self):
        """
        Update an answer column
        :return: bool:
        """
        con = psycopg2.connect(**self.config)
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            query = "UPDATE answers SET answer_body=%s WHERE answer_id=%s"
            cur.execute(query, (self.answer_body, self.answer_id))
            con.commit()
        except Exception as e:
            con.close()
            return False
        con.close()
        return True

    def delete(self):
        pass



class Question:
    def __init__(self, data={}):
        self.config = db_config()
        self.table, self.title = 'questions', data.get('title')
        self.body, self.q = data.get('body'), data.get('q')
        self.question_id = data.get('question_id')
        self.user_id = data.get('user_id')

    def save(self):
        """ Create a question record in questions table
        :return: None or record values
        """
        con = psycopg2.connect(**self.config)
        cur, response = con.cursor(cursor_factory=RealDictCursor), None
        try:
            query = "INSERT INTO questions (title, body, user_id) VALUES (%s, %s, %s) RETURNING *"
            cur.execute(query, (self.title, self.body, self.user_id))
            con.commit()
            response = cur.fetchone()
        except Exception as e:
            # print(e)
            con.close()
        con.close()
        return response

    def query(self):
        """Query the data in question table :return: list: query set list"""
        con, queryset_list = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            if not self.q:
                cur.execute(
                    " SELECT *,( SELECT count(*) FROM "
                    "answers WHERE answers.question_id=questions.question_id ) as "
                    "answers_count FROM questions "
                    " ORDER BY questions.created_at DESC"
                )
            else:
                query = "SELECT *, ( SELECT count(*) FROM answers WHERE "
                query += " answers.question_id=questions.question_id ) as answers_count "
                query += " FROM questions WHERE  body LIKE %s OR title LIKE %s  "
                query += " ORDER BY questions.created_at"
                cur.execute(query, (self.q, self.q))
            queryset_list = cur.fetchall()
        except Exception as e:
            con.close()
            # print(e)
        con.close()
        return queryset_list

    def filter_by(self):
        """
        Selects a question by id
        
        """
        con, queryset_list = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)
        cur2 = con.cursor(cursor_factory=RealDictCursor)

        try:
            query = """ SELECT * FROM questions WHERE questions.question_id=%s ORDER BY questions.created_at"""
            cur.execute(query % self.question_id)
            questions_queryset_list = cur.fetchall()
            cur2.execute("SELECT * FROM answers WHERE answers.question_id=%s" % self.question_id)
            answers_queryset_list = cur2.fetchall()
            queryset_list = {
                'question': questions_queryset_list,
                'answers': answers_queryset_list
            }
        except Exception as e:
            # print(e)
            con.close()
        con.close()
        return queryset_list

    def filter_by_user(self):
        """
        Selects question for specific user:default filters by current logged in user
        :return: False if record is not found else query list of found record
        """
        con, queryset_list = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                """ SELECT * FROM questions 
                    WHERE questions.user_id=""" + self.user_id + """ ORDER BY questions.created_at """
            )
            questions_queryset_list = cur.fetchall()
            queryset_list = {'question': questions_queryset_list}
        except Exception as e:
            # print(e)
            result = False
        con.close()
        return queryset_list

    def update(self):
        """
        Update an question column
        :return: bool:
        """
        con, result = psycopg2.connect(**self.config), True
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            query = "UPDATE questions SET title=%s, body=%s WHERE question_id=%s"
            cur.execute(query, (self.title, self.body, self.question_id))
            con.commit()
        except Exception as e:
            # print(e)
            result = False
        con.close()
        return result

    def record_exists(self):
        """
        checks whether a question was asked by the user
        :return: bool: False if record is not found else True
        """
        con, exists = psycopg2.connect(**self.config), False
        cur, queryset_list = con.cursor(cursor_factory=RealDictCursor), None
        try:
            query = "SELECT question_id, user_id FROM questions WHERE question_id=%s AND user_id=%s"
            cur.execute(query, (self.question_id, self.user_id))
            queryset_list = cur.fetchall()
            con.close()
            exists = True if len(queryset_list) >= 1 else False
        except Exception as e:
            # print(e)
            con.close()
        return exists

    def delete(self):
        """ Delete a table records
        :return: bool
        """
        con = psycopg2.connect(**self.config)
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            exist = self.filter_by()['question']
            if not len(exist) > 0:
                return 404
            if not self.record_exists():
                return 401
            cur.execute("DELETE from {} WHERE {}= '{}'".format(self.table, 'question_id', self.question_id))
            con.commit()
        except Exception as e:
            # print(e)
            con.close()
            return False
        con.close()
        return True
class User:
    def __init__(self, data={}):
        self.config = db_config()
        self.table, self.email = 'users', data.get('email')
        self.username = data.get('username')
        self.user_id = data.get('user_id')
        self.b_crypt = Bcrypt()
        if data.get('password'):
            self.password = self.b_crypt.generate_password_hash(data.get('password')).decode('utf-8')

    def query(self):
        con = psycopg2.connect(**self.config)
        cur = con.cursor(cursor_factory=RealDictCursor)
        cur.execute("select username, email, user_id, created_at from {}".format(self.table))
        queryset_list = cur.fetchall()
        con.close()
        return [item for item in queryset_list]

    def filter_by(self):
        con, queryset_list = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("select username, email, user_id, created_at from {} WHERE user_id='{}'".format(self.table, self.user_id))
            queryset_list = cur.fetchall()
        except Exception as e:
            # print(e)
            con.close()
        con.close()
        return queryset_list

    def filter_by_email(self):
        con, queryset_list = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("select * from {} WHERE email='{}'".format(self.table, self.email))
            queryset_list = cur.fetchall()
        except Exception as e:
            # print(e)
            con.close()
        con.close()
        return queryset_list

    def update(self):
        """
        Update an user column
        :return: bool:
        """
        con, result = psycopg2.connect(**self.config), True
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            query = "UPDATE users SET email=%s, username=%s WHERE user_id=%s"
            cur.execute(query, (self.email, self.username, self.user_id))
            con.commit()
        except Exception as e:
            # print(e)
            result = False
        con.close()
        return result

    def delete(self):
        con = psycopg2.connect(**self.config)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            query = "DELETE FROM users WHERE email=%s"
            cur.execute(query, self.email)
            con.commit()
            con.close()
        except Exception as e:
            # print(e)
            con.close()
            return False
        return True

    def save(self):
        con, response = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            query = "INSERT INTO users (username, email, password) values(%s, %s, %s) RETURNING *"
            cur.execute(query, (self.username, self.email, self.password))
            con.commit()
            response = cur.fetchone()
        except Exception as e:
            # print(e)
            con.close()
        con.close()
        return response
