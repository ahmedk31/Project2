from flask import Blueprint, request, jsonify
from .models import Doctor, Patient
from . import db

main = Blueprint('main', __name__)

@main.route('/add_doctor', methods=['POST'])
def add_doctor():
    name = request.json['name']
    specialization = request.json['specialization']
    doctor = Doctor(name=name, specialization=specialization)
    db.session.add(doctor)
    db.session.commit()
    return jsonify({'id': doctor.id, 'name': doctor.name, 'specialization': doctor.specialization})

@main.route('/add_patient', methods=['POST'])
def add_patient():
    name = request.json['name']
    age = request.json['age']
    gender = request.json['gender']
    doctor_id = request.json['doctor_id']
    room_number = request.json['room_number']
    bed_number = request.json['bed_number']
    patient = Patient(name=name, age=age, gender=gender, doctor_id=doctor_id, room_number=room_number, bed_number=bed_number)
    db.session.add(patient)
    db.session.commit()
    return jsonify({'id': patient.id, 'name': patient.name})
