from flask import Flask
from .migrations.db import db


def create_app(file):
    app = Flask(__name__)
    app.config.from_object(file)

    with app.app_context():
        pass

    # register our blueprints
    configure_blueprints(app)

    # register extensions
    configure_extensions()

    return app


def configure_blueprints(app):
    """ Configure blueprints . """
    from .api.questions.routes import question_blueprint
    from .api.auth.routes import auth_blueprint
    from .api.answers.routes import answers_blueprint
    from .api.users.routes import users_blueprint

    app_blueprints = [
        answers_blueprint,
        question_blueprint,
        auth_blueprint,
        users_blueprint
    ]

    for bp in app_blueprints:
        app.register_blueprint(bp)


def configure_extensions():
    db.migrate()


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)
