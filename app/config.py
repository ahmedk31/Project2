import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', None)
    MONGO_URI = os.getenv('MONGO_URI',None)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    MONGO_URI = os.getenv('MONGO_URI',None)