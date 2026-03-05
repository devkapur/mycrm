from pydantic import BaseModel, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime


class AuthCredentialCreate(BaseModel):
    password: str                           
    auth_provider: str = "LOCAL"  
 

class AuthCredentialResponse(BaseModel):
    id: UUID
    user_id: UUID
    auth_provider: str
    is_password_set: bool
    last_password_change: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}