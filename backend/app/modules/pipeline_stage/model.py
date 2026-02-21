from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text, Date, UniqueConstraint, Index, CheckConstraint, text,Integer, Numeric, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func 
from sqlalchemy.orm import relationship
from uuid_utils import uuid7
from app.core.database import Base

class PipelineStage(Base):
    __tablename__ = "pipeline_stages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7, server_default=text("gen_random_uuid()"), index=True)
    pipeline_id = Column(UUID(as_uuid=True), ForeignKey("pipelines.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    probability = Column(Integer, nullable=True, default=0)  # Probability of closing the deal at this stage (0-100)
    is_won_stage = Column(Boolean, nullable=False, default=False)  # Indicates if this stage is a "won" stage
    is_lost_stage = Column(Boolean, nullable=False, default=False)  # Indicates if this stage is a "lost" stage
    is_closed = Column(Boolean, nullable=False, default=False)  # Indicates if this stage is a closed stage (either won or lost)
    order_index = Column(Integer, nullable=True)  # Position of the stage within the pipeline
    custom_fields = Column(JSONB, nullable=True, default=dict)
    auto_actions = Column(JSONB, nullable=True, default=dict)  # Define any automatic actions/triggers for this stage
    color_code = Column(String(7), nullable=True)  # Optional color code for UI representation
    icon = Column(String(100), nullable=True)  # Optional icon for UI representation
    is_active = Column(Boolean, nullable=False, default=True)  # Indicates if this stage is active
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

     #====RELATIONSHIPS====
    pipeline = relationship("Pipeline", back_populates="stages")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_pipeline_stages")
    updater = relationship("User", foreign_keys=[updated_by], back_populates="updated_pipeline_stages")

    __table_args__ = (
        CheckConstraint('order_index IS NULL OR order_index>= 0', name='ck_pipeline_stage_display_order_positive'),
        UniqueConstraint("pipeline_id","name",name="uq_pipeline_stage_name_per_pipeline"),
        Index('ix_pipeline_stage_active', 'pipeline_id', 'name',
              postgresql_where=text("deleted_at IS NULL")),
    )

    def __repr__(self):
        return f"<PipelineStage(id={self.id}, name={self.name})>"