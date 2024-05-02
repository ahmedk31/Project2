import pytest
from app import create_app, db
from app.models import Doctor, Patient

@pytest.fixture
def app():
    """Setup the Flask application for testing."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # Use an in-memory database for testing
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    with app.app_context():
        db.create_all()  # Create tables for all registered models
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

def test_add_doctor(client):
    """Test adding a doctor."""
    doctor_data = {
        'name': 'Dr. Holmes',
        'specialization': 'Surgery'
    }
    response = client.post('/doctors', json=doctor_data)
    assert response.status_code == 201, "Should return a 201 status for a successful creation."
    json_data = response.get_json()
    assert json_data['name'] == 'Dr. Holmes', "The doctor's name should be returned in the response."

def test_get_doctors(client):
    """Test retrieving all doctors."""
    response = client.get('/doctors')
    assert response.status_code == 200, "Should return a 200 status for a successful fetch."
    doctors = response.get_json()
    assert isinstance(doctors, list), "The response should be a list of doctors."

def test_add_patient(client):
    """Test adding a patient."""
    # First, add a doctor since it's a foreign key for a patient
    doctor = Doctor(name="Dr. Holmes", specialization="Surgery")
    db.session.add(doctor)
    db.session.commit()

    # Now, test adding a patient
    patient_data = {
        'name': 'John Doe',
        'age': 30,
        'gender': 'Male',
        'doctor_id': doctor.id,
        'room_number': '100',
        'bed_number': '1'
    }
    response = client.post('/patients', json=patient_data)
    assert response.status_code == 201, "Should return a 201 status for a successful creation."
    json_data = response.get_json()
    assert json_data['name'] == 'John Doe', "The patient's name should be returned in the response."

def test_get_patients(client):
    """Test retrieving all patients."""
    response = client.get('/patients')
    assert response.status_code == 200, "Should return a 200 status for a successful fetch."
    patients = response.get_json()
    assert isinstance(patients, list), "The response should be a list of patients."
