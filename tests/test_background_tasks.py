import pytest
from app import create_app
from app.background_tasks import task_queue, start_worker, stop_worker, update_patient_record
from app.models import Patient
from app.database import db

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

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_worker():
    start_worker()
    yield
    stop_worker()

def test_process_update_task(app, worker):
    with app.app_context():
        # Setup a patient to update
        patient = Patient(name="John Doe", age=30, gender="Male", doctor_id=1)
        db.session.add(patient)
        db.session.commit()

        # Enqueue a task to update the patient
        updates = {'name': 'Jane Doe'}
        task_queue.put({'patient_id': patient.id, 'updates': updates})
        
        # Allow some time for the task to process
        import time; time.sleep(1)  # Not ideal for real tests, consider using mocks
        
        # Verify the update
        update_patient_record = Patient.query.get(patient.id)
        assert update_patient_record.name == 'Jane Doe', "Patient name should be updated to 'Jane Doe'"
