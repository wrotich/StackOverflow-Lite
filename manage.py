from flask_script import Manager
from app import create_app
from flask import jsonify,make_response
from app.migrations.db import db
import pytest
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app("config.BaseConfig")
manager = Manager(app)

@app.errorhandler(405)
def not_found():
    """
    return not found
    """
    return make_response(jsonify({"erro":"method not allowed"}))

@manager.command
def test():
    os.environ['APP_SETTINGS'] = 'TESTING'
    db.migrate_test_db()
    pytest.main(['-v', '--cov=app'])
    os.environ['APP_SETTINGS'] = 'PRODUCTION'
    db.drop_test_database()


if __name__ == "__main__":
    manager.run()