from typing import List
from fastapi import APIRouter, HTTPException, Body, status

from models.election import Election
from schemas.election import CreateElectionModel,ElectionResponse

router = APIRouter()

@router.post("/create", response_model=Election, status_code=status.HTTP_201_CREATED)
async def create_election(election_data: CreateElectionModel = Body(...)):
    election = Election(**election_data.dict())
    await election.insert()
    return election


@router.get("/by-organization/{organization_id}", response_model=List[ElectionResponse])
async def get_elections_by_organization(organization_id: str):
    elections = await Election.find(Election.organization_id == organization_id).to_list()
    if not elections:
        raise HTTPException(status_code=404, detail="No elections found for this organization")
    return elections