from flask import Blueprint, request, jsonify
from .models import Doctor, Patient, CheckHistory
from . import db
from datetime import datetime, timezone
from .models import Doctor, Patient, CheckHistory, User
from .background_tasks import task_queue


main = Blueprint('main', __name__)


@main.route('/')
def home():
    return 'Hello, World!'  #This is just to make the root directory

@main.route('/test') #This is for testing
def test():
    return 'Test Route'

@main.route('/register', methods=['POST'])
def register():
    data = request.json

    if 'username' not in data or 'email' not in data or 'password' not in data or 'role' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if data['role'] not in ['doctor', 'patient']:
        return jsonify({'error': 'Invalid role specified'}), 400

    user = User(username=data['username'], email=data['email'], role=data['role'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role}), 201

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


@main.route('/check_history', methods=['POST'])
def add_check_history():
    data = request.json
    check_history = CheckHistory(
        patient_id=data['patient_id'],
        check_time=data.get('check_time', datetime.now(timezone.utc))
    )
    db.session.add(check_history)
    db.session.commit()
    return jsonify({'id': check_history.id}), 201


@main.route('/update_patient/<int:patient_id>', methods=['POST'])
def update_patient(patient_id):
    updates = request.json
    task_queue.put({'patient_id': patient_id, 'updates': updates})
    return jsonify({"message": "Update in progress"}), 202