import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', None)  # Ensure this is set in production
    MONGO_URI = os.getenv('MONGO_URI', None)    # Ensure this is set in production
