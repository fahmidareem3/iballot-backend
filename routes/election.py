from typing import List,Union
from fastapi import APIRouter, HTTPException, Depends,Body, status
from beanie import PydanticObjectId
from models.election import Election
from schemas.election import CreateElectionModel,ElectionResponse,VoteCastingModel,CandidateVote,ScoreUpdateModel,CandidateInfoResponse,SingleCandidateResponse,MultipleCandidatesResponse
from models.user import User
from auth.jwt_handler import  decode_jwt
from auth.jwt_bearer import JWTBearer
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


@router.get("/{election_id}", response_model=ElectionResponse, dependencies=[Depends(JWTBearer())])
async def get_election_by_id(election_id: PydanticObjectId, token: str = Depends(JWTBearer())):
    election = await Election.get(election_id)
    if not election:
        raise HTTPException(status_code=404, detail="Election not found")
    return election

@router.get("/{election_id}/results", response_model=MultipleCandidatesResponse, status_code=status.HTTP_200_OK)
async def election_results(election_id: PydanticObjectId, token: str = Depends(JWTBearer())):
    election = await Election.get(election_id)
    if not election:
        raise HTTPException(status_code=404, detail="Election not found")

    if election.election_type == "Single":
        # Find the candidate with the highest votes
        winner = max(election.candidates, key=lambda candidate: candidate.votes)
        user = await User.get(PydanticObjectId(winner.user_id))
        if user:
            return MultipleCandidatesResponse(
                candidates=[CandidateInfoResponse(
                    id=user.id,
                    fullname=user.fullname,
                    email=user.email,
                    photoId=user.photoId,
                    userImage=user.userImage,
                    votes=winner.votes,
                    score=winner.score
                )]
            )

    elif election.election_type == "Multi":
        # Sort candidates based on votes
        sorted_candidates = sorted(election.candidates, key=lambda candidate: candidate.votes, reverse=True)
        winners_info = []
        for candidate in sorted_candidates:
            user = await User.get(PydanticObjectId(candidate.user_id))
            if user:
                winners_info.append(
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
        return MultipleCandidatesResponse(candidates=winners_info)

    elif election.election_type == "Score":
        # Sort candidates based on score
        sorted_candidates = sorted(election.candidates, key=lambda candidate: candidate.score, reverse=True)
        winners_info = []
        for candidate in sorted_candidates:
            user = await User.get(PydanticObjectId(candidate.user_id))
            if user:
                winners_info.append(
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
        return MultipleCandidatesResponse(candidates=winners_info)

    raise HTTPException(status_code=400, detail="Invalid election type")