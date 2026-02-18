from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, Integer, Date, Numeric, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, text
from uuid_utils import uuid7
from app.core.database import Base

class Contact(Base):
    __tablename__ = "contacts"
    

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7, server_default=text("gen_random_uuid()"), index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    first_name = Column(String(100), nullable=False, index=True)
    last_name = Column(String(100), nullable=False, index=True)
    full_name = Column(String(255), nullable=False, index=True)
    title = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True, index=True)
    mobile = Column(String(20), nullable=True)
    phone = Column(String(20), nullable=True)
    home_phone = Column(String(20), nullable=True)
    email_opt_out = Column(Boolean, nullable=False, default=False, index=True)
    description = Column(Text, nullable=True)
    date_of_birth = Column(Date, nullable=True, index=True)
    contact_type = Column(String(50), default="customer", index=True) # examples lead , prospect,customer,partner,vendor
    is_active = Column(Boolean, default=True, index=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id", ondelete="SET NULL"), nullable=True, index=True)
    
    mailing_street = Column(String(255), nullable=True)
    mailing_city = Column(String(100), nullable=True)
    mailing_state = Column(String(100), nullable=True)
    mailing_zip = Column(String(20), nullable=True)  
    mailing_country = Column(String(100), nullable=True)
    
    status = Column(String(50), nullable=False, default="new", index=True)
    lead_source = Column(String(50), nullable=True, index=True)
    
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    photo_url = Column(String(500), nullable=True)
    last_activity_time = Column(DateTime(timezone=True), nullable=True, index=True)
    next_follow_up_date = Column(Date, nullable=True, index=True)
    
    email_verified = Column(Boolean, default=False)

    social_media = Column(JSONB, nullable=True, default=dict)

    custom_fields = Column(JSONB, nullable=True, default=dict)
    tags = Column(ARRAY(String), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    tenant = relationship("Tenant", back_populates="contacts")
    account = relationship("Account", back_populates="contacts", foreign_keys=[account_id])
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_contacts")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_contacts")
    updater = relationship("User", foreign_keys=[updated_by], back_populates="updated_contacts")
    
    __table_args__ = (
        Index('uq_contact_tenant_email', 'tenant_id', 'email', unique=True, 
              postgresql_where=text("email IS NOT NULL AND deleted_at IS NULL")),
        Index('ix_contact_full_name_search','tenant_id', 'full_name', postgresql_using='gin', postgresql_ops={'full_name': 'gin_trgm_ops'}),
 	
    )
    
    def __repr__(self):
        return f"<Contact(id={self.id}, full_name={self.full_name}, email={self.email})>"