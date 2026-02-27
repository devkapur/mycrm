from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, CheckConstraint,text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid_utils import uuid7
from app.core.database import Base

class PipelineRecord(Base):
    __tablename__ = "pipeline_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7, server_default=text("gen_random_uuid()"), index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    pipeline_id = Column(UUID(as_uuid=True), ForeignKey("pipelines.id", ondelete="CASCADE"), nullable=False, index=True)
    stage_id = Column(UUID(as_uuid=True), ForeignKey("pipeline_stages.id", ondelete="SET NULL"), nullable=True, index=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id", ondelete="SET NULL"), nullable=True, index=True)
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True, index=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    status = Column(String(50), nullable=False, default="new", index=True)
    title = Column(String(255), nullable=False, index=True)
    value = Column(String(255), nullable=True, index=True)
    description = Column(Text, nullable=True)
    custom_fields = Column(JSONB, nullable=True, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    tenant = relationship("Tenant", back_populates="pipeline_records")
    pipeline = relationship("Pipeline", back_populates="records")
    stage = relationship("PipelineStage", back_populates="records")
    account = relationship("Account", back_populates="pipeline_records", foreign_keys=[account_id])
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_pipeline_records")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_pipeline_records")
    updater = relationship("User", foreign_keys=[updated_by], back_populates="updated_pipeline_records")

    def __repr__(self):
        return f"<PipelineRecord(id={self.id}, title={self.title})>"