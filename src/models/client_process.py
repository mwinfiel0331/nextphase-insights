from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ClientProcess:
    process_id: str
    client_id: str
    process_name: str
    process_description: str
    process_goal: str
    process_start: str
    process_end: str
    automation_needs: Optional[str]
    created_at: datetime
    updated_at: datetime