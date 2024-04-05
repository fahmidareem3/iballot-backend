from pydantic import BaseModel
from fastapi.security import HTTPBasicCredentials
from pydantic import EmailStr


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
            "example": {
                "fullname": "Fahmida Ara",
                "email": "fahmida@gmail.com",
            }
        }
