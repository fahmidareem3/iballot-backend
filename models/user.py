from typing import Optional
from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr


class User(Document):
    fullname: str
    email: EmailStr
    password: str
    institution: str
    role: str = "user"
    photoId: Optional[str] = None 
    userImage: Optional[str] = None  
    isverified: bool = False
    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Fahmida",
                "email": "fahmida@gmail.com",
                "password": "test",
                "role":"user",
                "institution": "CSEDU"
            }
        }

    class Settings:
        name = "user"


class UserSignIn(HTTPBasicCredentials):
    class Config:
        json_schema_extra = {
            "example": {"username": "fahmida@gmail.com", "password": "test"}
        }


class UserData(BaseModel):
    fullname: str
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {"email": "fahmida@gmail.com", "password": "test"}
        }
