from sqlalchemy import Column,Integer,String, Text, DateTime, Boolean, ForeignKey,UniqueConstraint, Index, CheckConstraint, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid_utils import uuid7
from datetime import datetime, timezone
from app.core.database import Base

class Profile(Base):
    __tablename__= "profiles"
     
    id = Column(UUID(as_uuid = True),primary_key = True,default = uuid7,server_default = text("gen_random_uuid()"))
    tenant_id = Column(UUID(as_uuid = True),ForeignKey("tenants.id", ondelete= "CASCADE"), nullable = False, index = True)
    name = Column(String(100), nullable = False, index = True)
    slug = Column(String(100), nullable = False, index = True)
    description = Column(Text, nullable = True)
    permissions = Column(JSONB, nullable = True, default = dict, server_default = '{}')
    is_system = Column(Boolean, nullable = False, default=False)
    is_default = Column(Boolean, nullable= False, default=False)
    is_active = Column(Boolean,nullable = False, default=True)
    settings = Column(JSONB, nullable = True, default = dict,server_default = '{}')
    created_at = Column(DateTime(timezone = True), nullable = False, server_default = func.now())
    created_by = Column(UUID(as_uuid = True),ForeignKey("users.id", ondelete = "SET NULL"),nullable = True)
    updated_at = Column(DateTime(timezone = True), nullable = False, server_default = func.now(), onupdate=func.now())
    updated_by = Column(UUID(as_uuid = True),ForeignKey("users.id", ondelete = "SET NULL"),nullable = True)
    deleted_at = Column(DateTime(timezone = True), nullable = True)

    tenant = relationship("Tenant", back_populates = "profiles")
    users = relationship("User", back_populates = "profile", foreign_keys = "User.profile_id")
    creator = relationship("User", foreign_keys = [created_by], back_populates = "created_profiles")
    updater = relationship("User", foreign_keys = [updated_by], back_populates = "updated_profiles")


    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name = "uq_profile_tenant_name"),
        UniqueConstraint("tenant_id", "slug", name = "uq_profile_tenant_slug"),
        Index("ix_profile_active", "is_active"),
        Index("ix_profiles_active_not_deleted", "is_active",postgresql_where = text("deleted_at IS NULL")),
        Index("ix_profile_system", "is_system"),
    )

    def __repr__(self):
        return f"<Profile(id={self.id}, name={self.name}, tenant_id={self.tenant_id})>"
    
    
