# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config  

db = SQLAlchemy()

def create_app(test_config=None):
    """Create and return a new Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(Config)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    db.init_app(app)

    return app
