from typing import List
from fastapi import Body, APIRouter, HTTPException,Depends
from passlib.context import CryptContext
from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import sign_jwt
from auth.jwt_handler import  decode_jwt
from database.database import add_user,update_user,get_user_by_id
from models.user import User
from schemas.user import UserData, UserSignIn, UserResponse,UserUpdate,UserInfoResponse,UserPublicData
from beanie import PydanticObjectId
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


@router.post("/signup", response_model=UserResponse)
async def user_signup(user: User = Body(...)):
    user_exists = await User.find_one(User.email == user.email)
    if user_exists:
        raise HTTPException(
            status_code=409, detail="User with email already exists"
        )

    user.password = hash_helper.encrypt(user.password)
    new_user = await add_user(user)
    print(new_user.id)
    token_response = sign_jwt(new_user.id)
    print(token_response)
    access_token = token_response["access_token"]
    return UserResponse(
        fullname=new_user.fullname,
        email=new_user.email,
        access_token=access_token
    )


@router.patch("/update", response_model=UserResponse)
async def update_user_details(
    user_update: UserUpdate = Body(...),
    token: str = Depends(JWTBearer())
):

    user_data = decode_jwt(token)
    user_id = PydanticObjectId(user_data['user_id'])
    existing_user = await User.get(user_id)
    print(existing_user)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.dict(exclude_none=True)
    if 'password' in update_data:
        update_data['password'] = hash_helper.hash(update_data['password'])

    updated_user = await update_user(user_id, update_data)
    return UserResponse(
        fullname=updated_user.fullname,
        email=updated_user.email,
        access_token=token  
    )

@router.get("/info", response_model=UserInfoResponse)
async def get_user_info(token: str = Depends(JWTBearer())):
    user_data = decode_jwt(token)
    user_id = PydanticObjectId(user_data['user_id'])
    existing_user = await User.get(user_id)

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Assuming UserInfoResponse is similar to UserResponse but without the access token
    return existing_user



@router.get("/getAll", response_model=List[UserPublicData])
async def get_all_users(token: str = Depends(JWTBearer())):
    
    user_data = decode_jwt(token)
    user_id = PydanticObjectId(user_data['user_id'])
    user = await User.get(user_id)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")

    users = await User.find_all().to_list()
    return users