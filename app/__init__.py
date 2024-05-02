from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app(config_class='Config'):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(f'instance.config.{config_class}')

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
