from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text, Date, UniqueConstraint, Index, CheckConstraint, text,Integer, Numeric, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from uuid_utils import uuid7
from app.core.database import Base

class Pipeline(Base):
    __tablename__ = "pipelines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7, server_default=text("gen_random_uuid()"), index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="active", index=True)
    is_default = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    pipeline_type = Column(String(50), nullable=True, default="sales", index=True)  # sales, support, onboarding
    currency = Column(String(10), nullable=True)
    allow_stage_skip = Column(Boolean, nullable=False, default=False)
    automation_rules = Column(JSONB, nullable=True, default=dict) 
    color_code = Column(String(7), nullable=True)
    icon = Column(String(100), nullable=True)
    display_order = Column(Integer, nullable=True)
    custom_fields = Column(JSONB, nullable=True, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
     
     #====RELATIONSHIPS====
    tenant = relationship("Tenant", back_populates="pipelines")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_pipelines")
    updater = relationship("User", foreign_keys=[updated_by], back_populates="updated_pipelines")

    __table_args__ = (
        Index('uq_pipeline_tenant_name', 'tenant_id', 'name', unique=True,
              postgresql_where=text("deleted_at IS NULL")),
        Index('ix_pipeline_active', 'tenant_id', 'status',
              postgresql_where=text("deleted_at IS NULL")),
        CheckConstraint('display_order >= 0', name='ck_pipeline_display_order_positive'),
    )

    def __repr__(self):
        return f"<Pipeline(id={self.id}, name={self.name})>"    