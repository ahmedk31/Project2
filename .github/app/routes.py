from flask import Blueprint, request, jsonify
from . import mongo
from .models import Doctor, Patient

main = Blueprint('main', __name__)

@main.route('/add_doctor', methods=['POST'])
def add_doctor():
    doctor_data = request.json
    doctor = Doctor(**doctor_data)
    result = mongo.db.doctors.insert_one(doctor.model_dump(exclude={'password'}))
    return jsonify({'id': str(result.inserted_id), 'message': 'Doctor added successfully'}), 201

@main.route('/add_patient', methods=['POST'])
def add_patient():
    patient_data = request.json
    patient = Patient(**patient_data)
    result = mongo.db.patients.insert_one(patient.model_dump(exclude={'password'}))
    return jsonify({'id': str(result.inserted_id), 'message': 'Patient added successfully'}), 201
