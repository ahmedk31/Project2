from app import create_app, db
from app.models import Doctor, Patient

def test_new_doctor():
    app = create_app('TestConfig')
    with app.app_context():
        doctor = Doctor(name='Dr. Strange', specialization='Magic')
        db.session.add(doctor)
        db.session.commit()
        assert Doctor.query.count() == 1

def test_new_patient():
    app = create_app('TestConfig')
    with app.app_context():
        doctor = Doctor(name='Dr. Strange', specialization='Magic')
        db.session.add(doctor)
        db.session.commit()
        patient = Patient(name='John Doe', age=30, gender='Male', doctor_id=doctor.id, room_number='101', bed_number='1A')
        db.session.add(patient)
        db.session.commit()
        assert Patient.query.count() == 1
