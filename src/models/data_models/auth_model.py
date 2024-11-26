from pydantic import BaseModel, EmailStr

class UserModel(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginModel(BaseModel):
    email: EmailStr
    password: str