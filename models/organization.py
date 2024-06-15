# In models/organization.py
from beanie import Document
from typing import List


class Organization(Document):
    name: str
    admin_id: str
    member_ids: List[str] = []
    membership_requests: List[str] = []

class Settings:
        name = "organization"