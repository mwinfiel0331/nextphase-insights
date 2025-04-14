from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ClientToolAssessment:
    client_id:str
    client_name:str
    communication_messaging:str
    task_project_management:str
    calendar_scheduling:str
    productivity:str
    crm:str
    ecom_payments:str
    data_analytics:str
    social_media_mgmt:str
    cloud:str
    marketing_advertising:str
    automation_workflow:str
    customer_support:str
    created_at:str
    updated_at:str
        }