from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from beanie import PydanticObjectId
class Candidate(BaseModel):
    user_id: str
    name: str
    votes: int = 0  

class CreateElectionModel(BaseModel):
    name: str = Field(..., example="2024 General Election")
    organization_id: str = Field(..., example="org12345")
    organization_name: str = Field(..., example="My Organization")
    start_time: datetime = Field(..., example="2024-01-01T00:00:00Z")
    end_time: datetime = Field(..., example="2024-12-31T23:59:59Z")
    candidates: List[Candidate] = []  

class ElectionResponse(BaseModel):
    id: PydanticObjectId
    name: str
    organization_id: str
    organization_name: str
    start_time: datetime
    end_time: datetime
    candidates: List[Candidate]

    class Config:
        orm_mode = True