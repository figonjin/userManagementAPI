from flask import Flask
from application.config import FlaskConfig
from application.extensions import db
from application.migrations.initialize import seed_db
from application.controllers.user_controller import user_controller


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    app.register_blueprint(user_controller)

    with app.app_context():
        db.create_all()
        seed_db()

    return app


if __name__ == "__main__":
    create_app(FlaskConfig).run(port=5000)
