from dataclasses import dataclass
from typing import List, Optional
from datetime import timedelta

@dataclass
class ProcessStep:
    step_number: int
    description: str
    performer: str
    tools: List[str]
    duration: str
    pain_points: str
    approvals: str
    screenshot: Optional[bytes] = None

@dataclass
class Process:
    process_name: str
    primary_goal: str
    start_trigger: str
    end_condition: str
    automation_desires: str
    tools_of_interest: str
    steps: List[ProcessStep]