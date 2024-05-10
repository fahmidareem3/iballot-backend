import datetime
from beanie import Document
from typing import List, Optional
from schemas.election import Candidate

class Election(Document):
    name: str
    organization_id: str
    organization_name: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    candidates: List[Candidate] = []

    class Settings:
        name = "elections"
        use_state_management = True 





