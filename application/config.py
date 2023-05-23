from flask import Config


class FlaskConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///userinfo.db"


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///testuserinfo.db"
    TESTING = True
