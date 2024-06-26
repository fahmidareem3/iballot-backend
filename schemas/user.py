from typing import Optional
from pydantic import BaseModel
from fastapi.security import HTTPBasicCredentials
from pydantic import EmailStr,Field

from beanie import PydanticObjectId
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


class UserResponse(BaseModel):
    fullname: str
    email: EmailStr
    access_token: str

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Fahmida Ara",
                "email": "fahmida@gmail.com",
                "access_token": "eyghojgdgjdlkjgldsjlajflkdjflsjlksjflkdsjflkdjfdkljfdklfjdkl"
            }
        }


class UserUpdate(BaseModel):
    fullname: Optional[str] = Field(None, example="Updated Name")
    email: Optional[EmailStr] = Field(None, example="updated@example.com")
    password: Optional[str] = Field(None, example="newpassword")
    institution: Optional[str] = Field(None, example="Updated Institution")
    photoId: Optional[str] = Field(None, example="new-photo-id")
    userImage: Optional[str] = Field(None, example="http://example.com/new-image.png")
    isverified: Optional[bool] = Field(None, example=False)



class UserInfoResponse(BaseModel):
    id: PydanticObjectId
    fullname: str
    email: EmailStr
    institution: Optional[str] = None
    role:str
    photoId: Optional[str] = None
    userImage: Optional[str] = None
    isverified: bool

    class Config:
        json_schema_extra = {
            "example": {
                "id": "60d0fe4f5311236168a109ca",
                "fullname": "Fahmida Ara",
                "email": "fahmida@gmail.com",
                "institution": "CSEDU",
                "photoId": "some-photo-id",
                "userImage": "http://example.com/image.png",
                "isverified": False
            }
        }


class UserPublicData(BaseModel):
    id: PydanticObjectId
    fullname: str
    email: EmailStr
    institution: Optional[str] = None
    role: str
    photoId: Optional[str] = None
    userImage: Optional[str] = None
    isverified: bool

    class Config:
        orm_mode = True