import pytest
from app import create_app
from app.database import db
from app.models import Doctor, Patient, User

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

def test_register_user(client):
    user_data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'newpassword',
        'role': 'doctor'  # Ensure role is explicitly set
    }
    response = client.post('/users/register', json=user_data)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['username'] == 'newuser'
    assert json_data['email'] == 'newuser@example.com'
    assert json_data['role'] == 'doctor'  # Verify role is correctly set and returned

def test_register_user_with_incomplete_data(client):
    incomplete_data = {
        'username': 'incompleteuser',
        # Missing role, email, and password to check 
    }
    response = client.post('/users/register', json=incomplete_data)
    assert response.status_code == 400
    assert 'error' in response.get_json()


def test_register_user_with_incomplete_data(client):
    incomplete_data = {
        'username': 'incompleteuser'
        # Missing email and password
    }
    response = client.post('/users/register', json=incomplete_data)
    assert response.status_code == 400
    assert 'error' in response.get_json()


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

def test_add_patient(client, app):
    """Test adding a patient."""
    with app.app_context():  # This ensures that the test is run within the application context
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


def test_add_check_history(client):
    # Assume a patient already exists with id=1 for this test to be meaningful
    check_data = {'patient_id': 1}
    response = client.post('/check_history', json=check_data)
    assert response.status_code == 201
    assert 'id' in response.get_json()

def test_add_doctor_error_handling(client):
    doctor_data = {'name': 'Dr. NoSpecialty'}  # Missing specialization
    response = client.post('/doctors', json=doctor_data)
    assert response.status_code == 400
    assert 'error' in response.get_json()
