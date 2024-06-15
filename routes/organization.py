from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException
from models.organization import Organization
from models.user import User
from auth.jwt_handler import  decode_jwt
from auth.jwt_bearer import JWTBearer
from schemas.organization import OrganizationResponse,OrganizationData,MembershipRequest,ApproveMembership
from beanie import PydanticObjectId
router = APIRouter()

@router.post("/create-organization", response_model=OrganizationResponse, dependencies=[Depends(JWTBearer())])
async def create_organization(organization: OrganizationData = Body(...), token: str = Depends(JWTBearer())):
    user_data = decode_jwt(token)
    user_id = PydanticObjectId(user_data['user_id'])
    user = await User.get(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="User is not authorized to create an organization")
    
    new_organization = Organization(
        name=organization.name,
        admin_id=str(user_id),  
         
    )
    await new_organization.create()
    return new_organization


@router.get("/getbyuser", response_model=List[OrganizationResponse])
async def get_organizations_by_user(token: str = Depends(JWTBearer())):
    user_data = decode_jwt(token)
    user_id = PydanticObjectId(user_data['user_id'])
    
    organizations = await Organization.find(Organization.admin_id == str(user_id)).to_list()
    
    if not organizations:
        raise HTTPException(status_code=404, detail="No organizations found for this user")
    
    return organizations



@router.post("/request-membership", dependencies=[Depends(JWTBearer())])
async def request_membership(request: MembershipRequest = Body(...), token: str = Depends(JWTBearer())):
    user_data = decode_jwt(token)
    user_id = PydanticObjectId(user_data['user_id'])
    
    organization = await Organization.get(request.organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if str(user_id) in organization.membership_requests:
        raise HTTPException(status_code=400, detail="Membership request already submitted")

    organization.membership_requests.append(str(user_id))
    await organization.save()
    return {"detail": "Membership request submitted successfully"}

@router.get("/{organization_id}", response_model=OrganizationResponse, dependencies=[Depends(JWTBearer())])
async def get_organization_by_id(organization_id: PydanticObjectId, token: str = Depends(JWTBearer())):
    organization = await Organization.get(organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization


@router.post("/approve-membership", dependencies=[Depends(JWTBearer())])
async def approve_membership(approve_request: ApproveMembership = Body(...), token: str = Depends(JWTBearer())):
    user_data = decode_jwt(token)
    admin_id = PydanticObjectId(user_data['user_id'])

    organization = await Organization.get(approve_request.organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if organization.admin_id != str(admin_id):
        raise HTTPException(status_code=403, detail="Only admins can approve membership requests")

    if str(approve_request.user_id) not in organization.membership_requests:
        raise HTTPException(status_code=404, detail="No such membership request found")

    organization.membership_requests.remove(str(approve_request.user_id))
    organization.member_ids.append(str(approve_request.user_id))
    await organization.save()
    return {"detail": "Membership request approved successfully"}
