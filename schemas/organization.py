from bson import ObjectId
from pydantic import BaseModel, Field, validator
from typing import List, Optional

class OrganizationResponse(BaseModel):
    name: str
    admin_id: str
    member_ids: List[str] 

    

class OrganizationData(BaseModel):
    name: str

    class Config:
        from_attributes = True  
