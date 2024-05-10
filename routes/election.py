from fastapi import APIRouter, HTTPException, Body, status

from models.election import Election
from schemas.election import CreateElectionModel

router = APIRouter()

@router.post("/create", response_model=Election, status_code=status.HTTP_201_CREATED)
async def create_election(election_data: CreateElectionModel = Body(...)):
    election = Election(**election_data.dict())
    await election.insert()
    return election
