from flask import Blueprint, request, jsonify
from .models import Doctor, Patient
from . import db

main = Blueprint('main', __name__)

@main.route('/doctors', methods=['POST'])
@main.route('/doctors', methods=['POST'])
def add_doctor():
    data = request.json
    if 'name' not in data or 'specialization' not in data:
        return jsonify({'error': 'Missing name or specialization'}), 400
    doctor = Doctor(name=data['name'], specialization=data['specialization'])
    db.session.add(doctor)
    db.session.commit()
    return jsonify({'id': doctor.id, 'name': doctor.name, 'specialization': doctor.specialization}), 201


@main.route('/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    results = [{'id': doc.id, 'name': doc.name, 'specialization': doc.specialization} for doc in doctors]
    return jsonify(results), 200

@main.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    patient = Patient(
        name=data['name'],
        age=data['age'],
        gender=data['gender'],
        doctor_id=data['doctor_id'],
        room_number=data['room_number'],
        bed_number=data['bed_number']
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify({'id': patient.id, 'name': patient.name}), 201

@main.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    results = [{'id': pat.id, 'name': pat.name, 'age': pat.age, 'gender': pat.gender, 'doctor_id': pat.doctor_id} for pat in patients]
    return jsonify(results), 200
