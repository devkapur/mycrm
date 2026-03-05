from pydantic import BaseModel
from pydantic import EmailStr, Field
from typing import Optional
from uuid import UUID


class OnboardingRequestDTO(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    domain: Optional[str] = Field(default=None, max_length=255)


class OnboardingResponseDTO(BaseModel):
    tenant_id: UUID
    organization_id: UUID
    user_id: UUID
    role_id: UUID
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
