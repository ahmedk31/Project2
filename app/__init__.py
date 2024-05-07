from flask import Flask
from .config import Config
from .database import db
from .routes import main
from .background_tasks import start_worker, stop_worker

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(main)


    with app.app_context():
        start_worker(app)

    @app.teardown_appcontext
    def cleanup(exception=None):
        stop_worker()


    return app
