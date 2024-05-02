from flask import Flask
from dotenv import load_dotenv
from .config import Config

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)
    
    if not app.config['SECRET_KEY']:
        raise ValueError("No SECRET_KEY set for Flask application")
    if not app.config['MONGO_URI']:
        raise ValueError("No MONGO_URI set for MongoDB connection")

    from .database import init_db
    init_db(app)
    
    from .routes import init_routes
    init_routes(app)
    
    return app
