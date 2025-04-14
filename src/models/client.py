from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Client:
    client_id: str
    company_name: str
    industry: str
    company_size: str
    contact_name: str
    contact_email: str
    contact_role: str
    created_at: datetime
    updated_at: datetime