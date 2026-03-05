from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from app.modules.user.model import UserStatus


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str

    

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    description: Optional[str] = None  
    website: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    fax: Optional[str] = None        
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None 
    timezone: Optional[str] = None
    language: Optional[str] = None
    time_format: Optional[str] = None 
    country_locale: Optional[str] = None 

    

class UserResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    email: str
    first_name: str
    last_name: str
    status: UserStatus
    email_verified: bool

    model_config = {"from_attributes": True}