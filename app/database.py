from pymongo import MongoClient
from flask import current_app as app


def init_db(app):
    if app.config['MONGO_URI']:
        app.db = MongoClient(app.config['MONGO_URI']).get_default_database()
    else:
        app.db = None  # Proper handling if no URI is provided


def add_doctor(data):
    result = app.db.doctors.insert_one(data)
    return str(result.inserted_id)

def get_all_doctors():
    return list(app.db.doctors.find({}))

def add_patient(data):
    result = app.db.patients.insert_one(data)
    return str(result.inserted_id)
