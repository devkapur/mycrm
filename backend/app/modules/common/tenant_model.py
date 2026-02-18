from uuid_utils import uuid7
import enum
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Text,
    Enum,
    CheckConstraint
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class TenantStatus(str,enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid7)
    name = Column(String(255), nullable=False)
    domain = Column(String(255), unique=True, nullable=True,index=True)
    status = Column(Enum(TenantStatus), nullable=False, default=TenantStatus.ACTIVE,index=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_source = Column(String(100),nullable=False, default="self_signup")
    data_region = Column(String(50), nullable=False, default="IN")
    timezone = Column(String(50), nullable=False, default="Asia/Kolkata")
    locale = Column(String(20), nullable=False, default="en_IN")
    tenant_metadata = Column(JSONB, nullable=True, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False,index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    users= relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    organizations = relationship("Organization", back_populates="tenant", cascade="all, delete-orphan")
    profiles = relationship("Profile", back_populates="tenant", cascade="all, delete-orphan")
    roles = relationship("Role", back_populates="tenant", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Tenant id={self.id} name={self.name} status={self.status}>"

