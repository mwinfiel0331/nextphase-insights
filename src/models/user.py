from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    user_id: str
    company_name: str
    email: str
    full_name: str
    app_role: str
    created_at: datetime
    updated_at: datetime
    password: Optional[str] = None  # Only used for creation/update