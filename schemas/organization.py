from bson import ObjectId
from pydantic import BaseModel, Field, validator
from typing import List, Optional

class OrganizationResponse(BaseModel):
    name: str
    admin_id: str
    member_ids: List[str]  # Confirm these should be strings, if not adjust accordingly

    

class OrganizationData(BaseModel):
    name: str

    class Config:
        orm_mode = True  # Adjust to from_attributes if using Pydantic v2
