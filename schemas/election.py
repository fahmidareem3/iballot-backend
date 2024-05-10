from pydantic import BaseModel, Field
from typing import List

class Candidate(BaseModel):
    user_id: str
    name: str
    votes: int = 0  # Initialize votes to zero

class CreateElectionModel(BaseModel):
    name: str = Field(..., example="2024 General Election")
    organization_id: str = Field(..., example="org12345")
    organization_name: str = Field(..., example="My Organization")
    candidates: List[Candidate] = []  # Optional: Start with an empty list or provide during creation
