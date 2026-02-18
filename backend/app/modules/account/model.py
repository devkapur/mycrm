from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text, Date, Enum, UniqueConstraint, Index, CheckConstraint, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid_utils import uuid7
from app.core.database import Base

class Account(Base):
    __tablename__ = "accounts"
    
    # === CORE IDENTITY ===
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7, server_default=text("gen_random_uuid()"), index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
  
    # === BASIC INFORMATION ===
    account_name = Column(String(255), nullable=False, index=True)
    website = Column(String(500), nullable=True)
    phone = Column(String(20), nullable=True)
    fax = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)  # General company email
    
    # === CLASSIFICATION ===
    account_type = Column(String(50), nullable=False, default="customer", index=True)
    industry = Column(String(100), nullable=True, index=True)
    sub_industry = Column(String(100), nullable=True)
    
    # === COMPANY DETAILS ===
    description = Column(Text, nullable=True)
    employees = Column(Integer, nullable=True)  # Number of employees
    annual_revenue = Column(Numeric(15, 2), nullable=True)  
 
    # === BILLING ADDRESS ===
    billing_street = Column(String(255), nullable=True)
    billing_city = Column(String(100), nullable=True)
    billing_state = Column(String(100), nullable=True)
    billing_zip = Column(String(20), nullable=True)
    billing_country = Column(String(100), nullable=True)
    
    # === SHIPPING ADDRESS ===
    shipping_street = Column(String(255), nullable=True)
    shipping_city = Column(String(100), nullable=True)
    shipping_state = Column(String(100), nullable=True)
    shipping_zip = Column(String(20), nullable=True)
    shipping_country = Column(String(100), nullable=True)
    
    # === OWNERSHIP & TERRITORY ===
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # === FINANCIAL INFO ===
    payment_terms = Column(String(50), nullable=True)  # "Net 30", "Net 60", "Due on Receipt"
    currency = Column(String(10), nullable=True,)
    
    # === TAX & LEGAL ===
    tax_id = Column(String(50), nullable=True)  # GST/VAT/EIN number
   
   
    # === SALES & PIPELINE ===
    status = Column(String(50), nullable=False, default="active", index=True)  # active, inactive, prospect
    lead_source = Column(String(50), nullable=True, index=True)
    account_score = Column(Integer, default=0, index=True)  # 0-100

    photo_url = Column(String(500), nullable=True)

    # === SOCIAL & WEB ===
    social_media = Column(JSONB, nullable=True, default=dict)
    
    # === FLEXIBILITY ===
    custom_fields = Column(JSONB, nullable=True, default=dict)
    tags = Column(ARRAY(String), nullable=True)
    
    # === TIMESTAMPS ===
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # === RELATIONSHIPS ===
    tenant = relationship("Tenant", back_populates="accounts")
    contacts = relationship("Contact", back_populates="account", foreign_keys="Contact.account_id")
    deals = relationship("Deal", back_populates="account")
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_accounts")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_accounts")
    updater = relationship("User", foreign_keys=[updated_by], back_populates="updated_accounts")
    
    __table_args__ = (
        # Unique account name per tenant
        Index('uq_account_tenant_name', 'tenant_id', 'account_name', unique=True,
              postgresql_where=text("deleted_at IS NULL")),
        
        # Full-text search
        Index('ix_account_name_search', 'account_name',
              postgresql_using='gin',
              postgresql_ops={'account_name': 'gin_trgm_ops'}),
        
        # Active accounts
        Index('ix_account_active', 'tenant_id', 'status',
              postgresql_where=text("deleted_at IS NULL")),
        
        CheckConstraint('employees >= 0', name='ck_account_employees_positive'),
        CheckConstraint('annual_revenue >= 0', name='ck_account_revenue_positive'),
    )
    
    def __repr__(self):
        return f"<Account(id={self.id}, name={self.account_name})>"