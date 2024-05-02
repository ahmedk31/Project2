from pydantic import BaseModel, EmailStr, Field, field_validator
import bcrypt

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str

    @field_validator('password', pre=True, always=True)
    def hash_password(cls, v):
        hashed_password = bcrypt.hashpw(v.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')

class Doctor(UserBase):
    specialization: str

class Patient(UserBase):
    age: int
    gender: str
    doctor_id: str
