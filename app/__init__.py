from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config, TestingConfig  

db = SQLAlchemy()

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    # Dynamically load the configuration specified by `config_class`
    app.config.from_object(config_class)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
