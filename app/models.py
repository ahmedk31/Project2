from pydantic import BaseModel

class Doctor(BaseModel):
    name: str
    specialization: str

class Patient(BaseModel):
    name: str
    age: int
    gender: str
    doctor_id: str
    room_number: int
    bed_number: int
