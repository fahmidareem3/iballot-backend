from fastapi import Body, APIRouter, HTTPException
from passlib.context import CryptContext

from auth.jwt_handler import sign_jwt
from database.database import add_user
from models.user import User
from schemas.user import UserData, UserSignIn, UserResponse

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/login")
async def user_login(user_credentials: UserSignIn = Body(...)):
    user_exists = await User.find_one(User.email == user_credentials.username)
    if user_exists:
        password_verified = hash_helper.verify(
            user_credentials.password, user_exists.password)
        if password_verified:
            token_response = sign_jwt(user_exists.id)
            access_token = token_response["access_token"]
            return UserResponse(
                fullname=user_exists.fullname,
                email=user_exists.email,
                access_token=access_token
            )

        raise HTTPException(
            status_code=403, detail="Incorrect email or password")

    raise HTTPException(status_code=403, detail="Incorrect email or password")


@router.post("/signup", response_model=UserData)
async def user_signup(user: User = Body(...)):
    user_exists = await User.find_one(User.email == user.email)
    if user_exists:
        raise HTTPException(
            status_code=409, detail="User with email already exists"
        )

    user.password = hash_helper.encrypt(user.password)
    new_user = await add_user(user)
    token_response = sign_jwt(new_user.id)
    access_token = token_response["access_token"]
    return UserResponse(
        fullname=new_user.fullname,
        email=new_user.email,
        access_token=access_token
    )
