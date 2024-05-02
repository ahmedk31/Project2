import pytest
from app import create_app, db
from app.models import Doctor, Patient

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    with app.app_context():
        db.create_all()
        # Pre-populate a doctor for associating with patients
        doctor = Doctor(name="Dr. Watson", specialization="General Surgery")
        db.session.add(doctor)
        db.session.commit()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_add_patient(client):
    # Retrieve the pre-populated doctor to use their ID
    doctor_id = Doctor.query.first().id

    # Patient details to be added
    patient_data = {
        'name': 'John Doe',
        'age': 34,
        'gender': 'Male',
        'doctor_id': doctor_id,
        'room_number': '12B',
        'bed_number': 'Bed 5'
    }

    # POST request to add a new patient
    response = client.post('/patients', json=patient_data)
    assert response.status_code == 201, "The patient should be added successfully."

    # Check the response data
    response_data = response.get_json()
    assert response_data['name'] == 'John Doe', "The name of the patient should match the input data."

    # Verify the patient is added in the database
    assert Patient.query.count() == 1, "There should be exactly one patient in the database."
