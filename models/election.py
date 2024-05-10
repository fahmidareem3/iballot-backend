from beanie import Document
from typing import List, Optional
from schemas.election import Candidate

class Election(Document):
    name: str
    organization_id: str
    organization_name: str
    candidates: List[Candidate] = []

    class Settings:
        name = "elections"
