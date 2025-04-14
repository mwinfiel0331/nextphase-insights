from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID

@dataclass
class ClientProcessStep:
    """Model representing a step in a client process"""
    step_id: str
    process_id: str
    client_id: str
    step_number: int
    description: str
    performer: str
    current_tools: List[str]
    desired_tools: List[str]
    duration: str
    pain_points: Optional[str] = None
    approvals: Optional[str] = None
    screenshot_url: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    def __post_init__(self):
        """Validate step data after initialization"""
        if not self.step_id:
            raise ValueError("Step ID is required")
        if not self.process_id:
            raise ValueError("Process ID is required")
        if not self.client_id:
            raise ValueError("Client ID is required")
        if self.step_number < 1:
            raise ValueError("Step number must be positive")
        if not self.description:
            raise ValueError("Description is required")
        if not self.performer:
            raise ValueError("Performer is required")
        if not self.duration:
            raise ValueError("Duration is required")
        
    @property
    def duration_minutes(self) -> Optional[int]:
        """Convert duration string to minutes if possible"""
        try:
            if 'hour' in self.duration.lower():
                hours = float(self.duration.split()[0])
                return int(hours * 60)
            elif 'min' in self.duration.lower():
                return int(self.duration.split()[0])
            return None
        except (ValueError, IndexError):
            return None

    def to_dict(self) -> dict:
        """Convert step to dictionary for Firestore"""
        return {
            'step_id': self.step_id,
            'process_id': self.process_id,
            'client_id': self.client_id,
            'step_number': self.step_number,
            'description': self.description,
            'performer': self.performer,
            'current_tools': self.current_tools,
            'desired_tools': self.desired_tools,
            'duration': self.duration,
            'pain_points': self.pain_points,
            'approvals': self.approvals,
            'screenshot_url': self.screenshot_url,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @staticmethod
    def from_dict(data: dict) -> 'ClientProcessStep':
        """Create step from Firestore dictionary"""
        return ClientProcessStep(**data)