from pydantic import BaseModel, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime


class RoleCreate(BaseModel):
    name: str                           
    description: Optional[str] = None  
    level: int                         
    reporting_to: Optional[UUID] = None 
    data_scope: str = "hierarchy"       
    share_with_peers: bool = False 

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    level: Optional[int] = None
    reporting_to: Optional[UUID] = None
    data_scope: Optional[str] = None
    share_with_peers: Optional[bool] = None
    is_active: Optional[bool] = None
    settings: Optional[dict] = None
    



class RoleResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    slug: str              
    description: Optional[str]
    level: int
    reporting_to: Optional[UUID]
    data_scope: str
    share_with_peers: bool
    is_system: bool
    is_default: bool
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}