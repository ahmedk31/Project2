from flask import Flask
from flask_pymongo import PyMongo
from config import DevelopmentConfig
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

mongo = PyMongo(app)

from app.routes import main as main_blueprint
app.register_blueprint(main_blueprint)
