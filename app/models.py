from .database import db
from datetime import datetime, timezone

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    patients = db.relationship('Patient', backref='doctor', lazy=True)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    room_number = db.Column(db.String(100))
    bed_number = db.Column(db.String(100))
    diagnosis = db.Column(db.String(255))
    prescribed_medicine = db.Column(db.String(255))

class CheckHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    check_time = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
