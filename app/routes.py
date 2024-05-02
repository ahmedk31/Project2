from flask import jsonify, request
from .database import add_doctor, get_all_doctors, add_patient

def init_routes(app):
    @app.route('/doctors', methods=['POST'])
    def create_doctor():
        doctor_data = request.get_json()
        doctor_id = add_doctor(doctor_data)
        return jsonify({"id": doctor_id}), 201

    @app.route('/doctors', methods=['GET'])
    def list_doctors():
        doctors = get_all_doctors()
        return jsonify(doctors), 200

    @app.route('/patients', methods=['POST'])
    def create_patient():
        patient_data = request.get_json()
        patient_id = add_patient(patient_data)
        return jsonify({"id": patient_id}), 201
