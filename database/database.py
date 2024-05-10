from typing import List, Union

from beanie import PydanticObjectId

from models.user import User


user_collection = User


async def add_user(new_user: User) -> User:
    user = await new_user.create()
    return user

async def get_user_by_id(user_id):
    return await User.find_one({"_id": user_id})

async def update_user(user_id, update_data):
    await User.find_one({"_id": user_id}).update({"$set": update_data})
    return await get_user_by_id(user_id)