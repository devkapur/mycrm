from pydantic import BaseModel
from typing import Dict,Optional
from uuid import UUID
from datetime import datetime

class ProfileCreate(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: Optional[dict] = None 

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[dict] = None  
    is_active: Optional[bool] = None


class ProfileResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    slug: str
    description: Optional[str]
    permissions: Optional[dict]
    is_system: bool
    is_default: bool
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True} 