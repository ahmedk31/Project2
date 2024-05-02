import pytest
from app import create_app, db
from app.models import Doctor, Patient

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a Flask application configured for testing
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # In-memory database
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    # Initialize the database
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
    

def test_doctor_creation(app):
    with app.app_context():
        doctor = Doctor(name="Dr. Holmes", specialization="Surgery")
        db.session.add(doctor)
        db.session.commit()
        assert Doctor.query.count() == 1

def test_patient_creation(app):
    with app.app_context():
        doctor = Doctor(name="Dr. Holmes", specialization="Surgery")
        db.session.add(doctor)
        db.session.commit()
        patient = Patient(name="John Doe", age=30, gender="Male", doctor_id=doctor.id, room_number="101", bed_number="1")
        db.session.add(patient)
        db.session.commit()
        assert Patient.query.count() == 1
