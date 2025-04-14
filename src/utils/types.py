from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ClientIntake:
    """Client intake form data model"""
    intake_id: str
    client_id: Optional[str]
    client_email: str
    business_description: Optional[str]
    current_challenges: Optional[str]
    primary_pain_point: Optional[str]
    optimization_goals: Optional[str]  # Added this field
    workflow_status: str = 'draft'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'ClientIntake':
        """Create ClientIntake from dictionary, handling timestamps"""
        # Convert Firestore timestamps if present
        if 'created_at' in data:
            data['created_at'] = data['created_at'].datetime() if hasattr(data['created_at'], 'datetime') else data['created_at']
        if 'updated_at' in data:
            data['updated_at'] = data['updated_at'].datetime() if hasattr(data['updated_at'], 'datetime') else data['updated_at']
        return cls(**data)