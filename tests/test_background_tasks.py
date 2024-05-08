import pytest
from app import create_app
from app.background_tasks import task_queue, start_worker, stop_worker
from app.models import Patient
from app.database import db
from threading import Event

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="module")
def worker(app):
    """Starts and stops the background worker for the duration of the module's tests."""
    start_worker(app)
    yield
    stop_worker()

def test_process_update_task(app, worker):
    with app.app_context():
        # Create a patient record to update.
        patient = Patient(name="John Doe", age=30, gender="Male", doctor_id=1)
        db.session.add(patient)
        db.session.commit()

        # Set up synchronization with an Event object.
        done_event = Event()
        updates = {'name': 'Jane Doe'}
        task_queue.put({'patient_id': patient.id, 'updates': updates, 'event': done_event})

        # Wait for the event to be signaled by the background worker indicating the update is complete.
        done_event.wait(timeout=10)  # Timeout to avoid hanging indefinitely.

        # Fetch the patient again to verify updates.
        db.session.expire_all()  # Invalidate the session cache to ensure fresh data is fetched.
        updated_patient_record = Patient.query.get(patient.id)

        # Assert the patient's name has been updated as expected.
        assert updated_patient_record.name == 'Jane Doe', "Patient name should be updated to 'Jane Doe'"
