from typing import List
from fastapi import APIRouter, HTTPException, Body, status

from models.election import Election
from schemas.election import CreateElectionModel,ElectionResponse,VoteCastingModel,CandidateVote

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


@router.post("/vote", status_code=status.HTTP_200_OK)
async def cast_vote(vote_data: VoteCastingModel = Body(...)):
    
    election = await Election.get(vote_data.election_id)
    print(election)
    if not election:
        raise HTTPException(status_code=404, detail="Election not found")

    for candidate in election.candidates:
        if candidate.user_id == vote_data.candidate_user_id:
            candidate.votes += 1
            await election.save_changes()
            return CandidateVote(**candidate.dict())

    raise HTTPException(status_code=404, detail="Candidate not found")
