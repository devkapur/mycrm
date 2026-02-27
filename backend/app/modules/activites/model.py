from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, CheckConstraint,text,Index  
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid_utils import uuid7
from app.core.database import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7, server_default=text("gen_random_uuid()"), index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False, index=True)  # e.g. "pipeline_record", "account", etc.
    entity_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    action = Column(String(50), nullable=False, index=True)  # e.g. "created", "updated", "deleted", etc.
    description = Column(Text, nullable=True)
    type = Column(String(50), nullable=True)  # e.g. "system", "user", etc.
    status = Column(String(50), nullable=True, index=True)
    priority = Column(String(50), nullable=True, index=True)
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    reminder_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    custom_fields = Column(JSONB, nullable=True, default=dict)
    notes = Column(Text, nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    tenant = relationship("Tenant", back_populates="activities")
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_activities")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_activities")
    
    __table_args__ = (
        Index('ix_activity_entity', 'entity_type', 'entity_id'),
        Index('ix_activity_status', 'status'),
        )
    def __repr__(self):
        return f"<Activity(id={self.id}, entity_type={self.entity_type}, entity_id={self.entity_id})>"