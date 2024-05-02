from . import db

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    room_number = db.Column(db.String(100))
    bed_number = db.Column(db.String(100))
