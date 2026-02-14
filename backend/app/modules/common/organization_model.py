from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from uuid_utils import uuid7
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(UUID(as_uuid=True),primary_key=True,index=True, default=uuid7,server_default=func.gen_random_uuid())
    tenant_id = Column(UUID(as_uuid = True),ForeignKey("tenants.id",ondelete="CASCADE"),nullable=False,unique=True,index=True)
    company_name = Column(String(255),nullable=False, index=True)
    alias = Column(String(255),nullable=True)
    website = Column(String(255),nullable=True)
    description = Column(Text,nullable=True)
    primary_email = Column(String(255),nullable=True)
    phone = Column(String(255),nullable=True)
    mobile = Column(String(255),nullable=True)
    fax = Column(String(255),nullable=True)
    street = Column(String(255),nullable=True)
    city = Column(String(255),nullable=True)
    state = Column(String(255),nullable=True)
    zip = Column(String(255),nullable=True)
    country = Column(String(255),nullable=True)
    country_code = Column(String(5),nullable=True)
    currency_code = Column(String(10),nullable=True)
    currency_symbol = Column(String(10),nullable=True)
    currency_locale = Column(String(10),nullable=True)
    timezone = Column(String(100),nullable=True)
    employees_count = Column(Integer,nullable=True)
    industry = Column(String(255),nullable=True)
    tax_id = Column(String(255),nullable=True)
    logo_file_id = Column(UUID(as_uuid=True),nullable=True)
    settings = Column(JSONB,nullable=True,default=dict)
    is_active = Column(Boolean,nullable=False,default=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True),nullable=True)

    tenant = relationship("Tenant", back_populates="organizations")

    def __repr__(self) -> str:
        return f"<Organization id={self.id} company_name={self.company_name} is_active={self.is_active}>"
    
