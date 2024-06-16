from typing import List
from fastapi import APIRouter, HTTPException, Body, status
from beanie import PydanticObjectId
from models.election import Election
from schemas.election import CreateElectionModel,ElectionResponse,VoteCastingModel,CandidateVote,ScoreUpdateModel,CandidateInfoResponse
from models.user import User
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


@router.post("/update-score", status_code=status.HTTP_200_OK)
async def update_candidate_score(score_data: ScoreUpdateModel = Body(...)):
    
    election = await Election.get(score_data.election_id)
    if not election:
        raise HTTPException(status_code=404, detail="Election not found")

    
    for candidate in election.candidates:
        if candidate.user_id == score_data.candidate_user_id:
            candidate.score = (candidate.score or 0) + score_data.additional_score
            await election.save_changes()
            return {"detail": "Score updated successfully", "new_score": candidate.score}

    raise HTTPException(status_code=404, detail="Candidate not found")


@router.get("/{election_id}/candidates", response_model=List[CandidateInfoResponse], status_code=status.HTTP_200_OK)
async def get_candidates(election_id: PydanticObjectId):
    election = await Election.get(election_id)
    if not election:
        raise HTTPException(status_code=404, detail="Election not found")
    
    candidates_info = []
    for candidate in election.candidates:
        user = await User.get(PydanticObjectId(candidate.user_id))
        if user:
            candidates_info.append(
                CandidateInfoResponse(
                    id=user.id,
                    fullname=user.fullname,
                    email=user.email,
                    photoId=user.photoId,
                    userImage=user.userImage,
                    votes=candidate.votes,
                    score=candidate.score
                )
            )
    return candidates_info
