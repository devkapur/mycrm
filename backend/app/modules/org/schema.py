from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime


class OrganizationCreate(BaseModel):
    company_name: str
    alias: Optional[str] = None
    phone: Optional[str] = None
    primary_email: Optional[EmailStr] = None  
  
                      
class OrganizationUpdate(BaseModel):
    company_name: Optional[str] = None
    alias: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    primary_email: Optional[EmailStr] = None  
    phone: Optional[str] = None
    mobile: Optional[str] = None
    fax: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    currency_code: Optional[str] = None
    currency_symbol: Optional[str] = None
    currency_locale: Optional[str] = None
    timezone: Optional[str] = None
    employees_count: Optional[int] = None
    industry: Optional[str] = None
    tax_id: Optional[str] = None
    settings: Optional[dict] = None


class OrganizationResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    company_name: str
    alias: Optional[str]
    website: Optional[str]
    primary_email: Optional[str]
    phone: Optional[str]
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}