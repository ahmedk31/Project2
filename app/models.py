from . import db
from pydantic import BaseModel, EmailStr
import bcrypt

# SQLAlchemy models
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    specialization = db.Column(db.String(255), nullable=False)
    patients = db.relationship('Patient', backref='doctor', lazy=True)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    room_number = db.Column(db.String(100))
    bed_number = db.Column(db.String(100))

# Pydantic models for request validation
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserDisplay(UserBase):
    id: int

    class Config:
        orm_mode = True
