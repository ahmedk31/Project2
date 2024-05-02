from flask import Blueprint, request, jsonify
from . import db
from .models import Doctor, Patient, User, UserCreate

main = Blueprint('main', __name__)

@main.route('/register', methods=['POST'])
def register():
    user_data = request.get_json()
    user = UserCreate(**user_data)  # Validate incoming data
    new_user = User(email=user.email, username=user.username)
    new_user.set_password(user.password)  # Hash the password
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"username": new_user.username, "email": new_user.email}), 201

@main.route('/doctors', methods=['POST'])
def add_doctor():
    data = request.get_json()
    doctor = Doctor(name=data['name'], specialization=data['specialization'])
    db.session.add(doctor)
    db.session.commit()
    return jsonify({'id': doctor.id, 'name': doctor.name, 'specialization': doctor.specialization}), 201

@main.route('/patients', methods=['POST'])
def add_patient():
    data = request.get_json()
    patient = Patient(
        name=data['name'], age=data['age'], gender=data['gender'],
        doctor_id=data['doctor_id'], room_number=data['room_number'], bed_number=data['bed_number']
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify({'id': patient.id, 'name': patient.name}), 201
