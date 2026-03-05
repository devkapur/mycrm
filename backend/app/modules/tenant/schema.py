from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.modules.tenant import TenantStatus


class TenantCreate(BaseModel):
    name: str
    domain: Optional[str] = None
    created_source: Optional[str] = "self_signup"
    data_region: Optional[str] = "IN"
    timezone: Optional[str] = "Asia/Kolkata"
    locale: Optional[str] = "en_IN"
    tenant_metadata: Optional[dict] = {}
    
    model_config = {"from_attributes": True}



class TenantUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    status: Optional[TenantStatus] = None
    is_active: Optional[bool] = None
    created_source: Optional[str] = None
    data_region: Optional[str] = None
    timezone: Optional[str] = None
    locale: Optional[str] = None
    tenant_metadata: Optional[dict] = {}

    model_config = {"from_attributes": True}

class TenantResponse(BaseModel):
    id: UUID
    name: str
    domain: Optional[str] = None
    status: TenantStatus
    is_active: bool
    created_source: str
    data_region: str
    timezone: str
    locale: str
    tenant_metadata: dict
    created_at: datetime
    updated_at: datetime
 

    model_config = {"from_attributes": True}