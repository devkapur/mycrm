import enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, UniqueConstraint,Enum
from uuid_utils import uuid7
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.modules.common.tenant_model import Tenant
from app.core.database import Base

class UserStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"
    deleted = "deleted"
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid = True), primary_key = True, index = True, default = uuid7)
    tenant_id = Column(UUID(as_uuid = True), ForeignKey("tenants.id",ondelete="CASCADE"),nullable = False, index = True)
    email = Column(String(255), nullable = False, index = True)
    email_verified = Column(Boolean, nullable = False, default = False)
    email_verified_at = Column(DateTime(timezone = True), nullable = True)
    first_name = Column(String(100), nullable = False)
    last_name = Column(String(100), nullable = False)
    website = Column(String(255), nullable = True)
    description = Column(Text, nullable = True)
    phone = Column(String(20), nullable = True)
    mobile = Column(String(20), nullable = True)
    fax = Column(String(20), nullable = True)
    status = Column(Enum(UserStatus), nullable = False, default = UserStatus.active, index = True)
    role_id = Column(UUID(as_uuid = True), ForeignKey("roles.id",ondelete= "SET NULL", use_alter=True, name="fk_users_role_id"), nullable = True, index = True)
    profile_id = Column(UUID(as_uuid = True), ForeignKey("profiles.id", ondelete = "SET NULL", use_alter=True, name="fk_users_profile_id"), nullable = True, index = True)
    street = Column(String(100), nullable = True)
    city = Column(String(100), nullable = True)
    state = Column(String(100), nullable = True)
    zip = Column(String(20), nullable = True)
    country = Column(String(100), nullable = True)
    country_code = Column(String(10), nullable = True)
    language = Column(String(20), nullable = True)
    country_locale = Column(String(20), nullable = True)
    time_format = Column(String(20), nullable = True)
    timezone = Column(String(100), nullable = True)
    settings = Column(JSONB, nullable = True, default = dict)
    last_login_at = Column(DateTime(timezone = True), nullable = True)
    created_at = Column(DateTime(timezone = True), server_default = func.now(), nullable = False)
    created_by = Column(UUID(as_uuid = True), ForeignKey("users.id", ondelete = "SET NULL"), nullable = True, index = True)
    updated_at = Column(DateTime(timezone = True), server_default = func.now(), onupdate = func.now(), nullable = False)
    updated_by = Column(UUID(as_uuid = True), ForeignKey("users.id", ondelete = "SET NULL"), nullable = True, index = True)
    deleted_at = Column(DateTime(timezone = True), nullable = True)
    
    __table_args__ =(
        UniqueConstraint("tenant_id", "email", name = "uq_user_tenant_email"),
    )
    
    tenant = relationship("Tenant", back_populates="users")
    role = relationship("Role", back_populates="users")
    profile = relationship("Profile", back_populates="users")
    created_by_user = relationship("User", remote_side=[id],foreign_keys=[created_by], backref="created_users")
    updated_by_user = relationship("User", remote_side=[id], foreign_keys=[updated_by], backref="updated_users")  
    created_roles = relationship("Role", foreign_keys="Role.created_by", back_populates="creator")
    updated_roles = relationship("Role", foreign_keys="Role.updated_by", back_populates="updater")
    created_profiles = relationship("Profile", foreign_keys="Profile.created_by", back_populates="creator")
    updated_profiles = relationship("Profile", foreign_keys="Profile.updated_by", back_populates="updater")


    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} tenant_id={self.tenant_id}>"
    