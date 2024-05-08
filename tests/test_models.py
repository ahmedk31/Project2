import pytest,bcrypt
from app import create_app
from app.database import db
from app.models import Doctor, Patient, CheckHistory,User
from app.background_tasks import task_queue
from sqlalchemy import select


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
    


def test_user_creation_and_password_hashing(app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com", role='doctor')
        user.set_password("securepassword")
        db.session.add(user)
        db.session.commit()

        saved_user = db.session.execute(select(User).filter_by(username="testuser")).scalar_one()
        assert saved_user is not None
        assert bcrypt.checkpw("securepassword".encode('utf-8'), saved_user.password_hash)


def test_password_check(app):
    with app.app_context():
        user = User(username="testuser2", email="test2@example.com", role='patient')
        user.set_password("securepassword123")
        db.session.add(user)
        db.session.commit()

        assert user.check_password("securepassword123") == True
        assert user.check_password("wrongpassword") == False


def test_user_role_assignment(app):
    with app.app_context():
        user_doctor = User(username="docexample", email="doc@example.com", role="doctor")
        user_doctor.set_password("securepassword123")
        db.session.add(user_doctor)

        user_patient = User(username="patientexample", email="patient@example.com", role="patient")
        user_patient.set_password("securepassword123")
        db.session.add(user_patient)
        db.session.commit()

        saved_doctor = db.session.execute(select(User).filter_by(username="docexample")).scalar_one()
        saved_patient = db.session.execute(select(User).filter_by(username="patientexample")).scalar_one()

        assert saved_doctor.role == "doctor"
        assert saved_patient.role == "patient"


def test_doctor_creation(app):
    with app.app_context():
        doctor = Doctor(name="Dr. Holmes", specialization="Surgery")
        db.session.add(doctor)
        db.session.commit()
        doctor_count = db.session.execute(select(Doctor)).scalars().all()
        assert len(doctor_count) == 1


def test_patient_creation(app):
    with app.app_context():
        doctor = Doctor(name="Dr. Holmes", specialization="Surgery")
        db.session.add(doctor)
        db.session.commit()
        patient = Patient(name="John Doe", age=30, gender="Male", doctor_id=doctor.id, room_number="101", bed_number="1")
        db.session.add(patient)
        db.session.commit()
        patient_count = db.session.execute(select(Patient)).scalars().all()
        assert len(patient_count) == 1


def test_relationships(app):
    with app.app_context():
        doctor = Doctor(name="Dr. Wise", specialization="General")
        db.session.add(doctor)
        db.session.commit()

        patient = Patient(name="John Doe", age=30, gender="Male", doctor_id=doctor.id)
        db.session.add(patient)
        db.session.commit()

        assert patient.doctor == doctor  # Check if the relationship is correctly established


def test_default_check_time(app):
    with app.app_context():
        patient = Patient(name="John Doe", age=30, gender="Male", doctor_id=1)
        db.session.add(patient)
        db.session.commit()
        check_history = CheckHistory(patient_id=patient.id)
        db.session.add(check_history)
        db.session.commit()
        assert check_history.check_time is not None


def test_queue_update_patient_record(app):
    with app.app_context():
        initial_queue_size = task_queue.qsize()  # Getting the initial size of the queue
        task_queue.put({'patient_id': 1, 'updates': {'name': 'Updated Name'}})
        assert task_queue.qsize() == initial_queue_size + 1, "Task should be added to the queue"