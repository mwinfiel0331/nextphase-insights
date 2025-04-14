from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ClientIntake:
    intake_id: str
    client_id: str
    business_description: str
    current_challenges: str
    primary_pain_point: str
    optimization_goals: str
    workflow_status: str
    created_at: datetime
    updated_at: datetime