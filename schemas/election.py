from pydantic import BaseModel, Field,EmailStr
from typing import List, Optional
from datetime import datetime
from beanie import PydanticObjectId
class Candidate(BaseModel):
    user_id: str
    votes: int = 0
    score: Optional[int] = 0   

class CreateElectionModel(BaseModel):
    name: str = Field(..., example="2024 General Election")
    organization_id: str = Field(..., example="org12345")
    organization_name: str = Field(..., example="My Organization")
    election_type: str= Field(..., example="Single Vote")
    start_time: datetime = Field(..., example="2024-01-01T00:00:00Z")
    end_time: datetime = Field(..., example="2024-12-31T23:59:59Z")
    candidates: List[Candidate] = []  

class ElectionResponse(BaseModel):
    id: PydanticObjectId
    name: str
    organization_id: str
    organization_name: str
    election_type: str
    start_time: datetime
    end_time: datetime
    candidates: List[Candidate]

    class Config:
        orm_mode = True


class VoteCastingModel(BaseModel):
    election_id: PydanticObjectId
    candidate_user_id: str

class CandidateVote(BaseModel):
    user_id: str
    votes: int

    class Config:
        orm_mode = True

class ScoreUpdateModel(BaseModel):
    election_id: PydanticObjectId
    candidate_user_id: str
    additional_score: int = Field(..., example=5, description="The score to add to the candidate's total.")


class CandidateInfoResponse(BaseModel):
    id: PydanticObjectId
    fullname: str
    email: EmailStr
    photoId: Optional[str]
    userImage: Optional[str]
    votes: int
    score: Optional[int]