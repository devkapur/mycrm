from sqlalchemy import ( 
    Column, String, Text, DateTime,Boolean, ForeignKey,
    UniqueConstraint,Index,CheckConstraint,text,Integer
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid_utils import uuid7
from datetime import datetime
from app.core.database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True),primary_key = True, index = True, default = uuid7,server_default = text("gen_random_uuid()"))
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable = False, index=True)
    name = Column(String(25), nullable = False , index = True)
    slug = Column(String(25), nullable = False , index = True)
    description = Column(Text, nullable = True)
    reporting_to = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="SET NULL"), nullable = True, index = True)
    level = Column(Integer, nullable = False, index = True)
    data_scope = Column(String(20), nullable = False, default = "hierarchy", index = True)
    share_with_peers = Column(Boolean , default = False, nullable = False)
    is_system = Column(Boolean, default = False, nullable = False)
    is_default = Column(Boolean, default = False, nullable = False)
    is_active = Column(Boolean, default = True, nullable = False)
    settings = Column(JSONB, nullable = True, default = dict)
    created_at = Column(DateTime(timezone = True), server_default = func.now(), nullable = False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable = True, index = True)
    updated_at = Column(DateTime(timezone = True), server_default = func.now(), onupdate = func.now(), nullable = False)
    updated_by = Column(UUID(as_uuid= True), ForeignKey("users.id", ondelete="SET NULL"), nullable = True )
    deleted_at = Column(DateTime(timezone = True), nullable = True)
   
    tenant = relationship("Tenant", back_populates="roles")
    manager_role = relationship("Role", remote_side=[id], back_populates="subordinate_roles")
    subordinate_roles = relationship("Role", back_populates="manager_role",foreign_keys=[reporting_to]) 
    users = relationship("User", back_populates="role",foreign_keys="User.role_id")
    role_permissions = relationship("RolePermission", back_populates="role",cascade = "all, delete-orphan")
    creator = relationship("User",foreign_keys=[created_by], back_populates = "created_roles")
    updater = relationship("User",foreign_keys = [updated_by], back_populates = "updated_roles")

    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name = "uq_role_tenant_name"),
        UniqueConstraint("tenant_id", "slug", name = "uq_role_tenant_slug"),
        CheckConstraint("level > 0", name = "ck_role_level_non_negative"),
        CheckConstraint(
        "data_scope IN ('all', 'hierarchy', 'own', 'team')",
          name = "check_role_data_scope"
          ).
        Index("ix_role_active","is_active"),
        Index("ix_role_level", "level"),
        Index("ix_roles_active_not_deleted", "is_active",postgresql_where = text("deleted_at IS NULL")),

    )
    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name}, level={self.level})>"