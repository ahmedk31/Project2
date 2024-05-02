import pytest
from app import create_app, db
from app.models import Doctor, Patient

@pytest.fixture
def app():
    app = create_app('Config')
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_new_doctor(app):
    with app.app_context():
        doctor = Doctor(name="Dr. Watson", specialization="General")
        db.session.add(doctor)
        db.session.commit()
        assert Doctor.query.count() == 1

def test_new_patient(app):
    with app.app_context():
        doctor = Doctor(name="Dr. Watson", specialization="General")
        db.session.add(doctor)
        db.session.commit()
        patient = Patient(name="John Doe", age=30, gender="Male", doctor_id=doctor.id, room_number="100", bed_number="1")
        db.session.add(patient)
        db.session.commit()
        assert Patient.query.count() == 1
