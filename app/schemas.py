#Disregar this file for now
from pydantic import BaseModel, EmailStr, field_validator
import bcrypt

class UserBase(BaseModel):
    role: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str

    @field_validator('password')
    def hash_password(cls, v):
        return bcrypt.hashpw(v.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
