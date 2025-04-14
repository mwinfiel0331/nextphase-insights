from dataclasses import dataclass
from typing import List, Optional
from datetime import timedelta, datetime

@dataclass
class ProcessStep:
    step_number: int
    description: str
    performer: str
    current_tools: List[str]
    desired_tools: List[str]
    duration: str
    pain_points: str
    approvals: str
    screenshot: Optional[bytes] = None
    created_at: datetime = datetime.now()


@dataclass
class Process:
    process_name: str
    process_goal: str
    process_start: str
    process_end: str
    automation_needs: str
    steps: List[ProcessStep]
    created_at: datetime = datetime.now()


@dataclass
class ProcessSection:
    """Process section model"""
    section_id: str
    process_id: str
    section_name: str
    section_description: str
    section_order: int
    expected_duration: str
    dependencies: List[str]
    owner: str
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

