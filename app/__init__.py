from flask import Flask
from .config import Config
from .database import db
from .routes import main
from .task_manager import stop_worker_threads, start_worker_threads


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


    threads = start_worker_threads(5)

    @app.teardown_appcontext
    def cleanup(response_or_exc):
        stop_worker_threads(threads)
        return response_or_exc

    return app
