from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, CheckConstraint,text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid_utils import uuid7
from app.core.database import Base

class AuthCredential(Base):
    __tablename__ = "auth_credentials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7, server_default=text("gen_random_uuid()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    auth_provider = Column(String(20), nullable=False, default="LOCAL", index=True)
    password_hash = Column(Text, nullable=True)  
    password_algo = Column(String(20), nullable=True)  
    is_password_set = Column(Boolean, nullable=False, default=False)
    last_password_change = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

  
    user = relationship("User", back_populates="auth_credential")

    __table_args__ = (
        CheckConstraint(
            "auth_provider IN ('LOCAL', 'GOOGLE', 'AZURE', 'OKTA', 'GITHUB', 'SAML', 'OAUTH')",
            name="ck_auth_provider_valid"
        ),
        CheckConstraint(
            "password_algo IN ('bcrypt', 'argon2id') OR password_algo IS NULL",
            name="ck_password_algo_valid"
        ),
        CheckConstraint(
            "(is_password_set = true AND password_hash IS NOT NULL AND password_algo IS NOT NULL) OR "
            "(is_password_set = false AND password_hash IS NULL AND password_algo IS NULL)",
            name="ck_password_consistency"
        ),
    )

    def __repr__(self):
        return f"<AuthCredential(id={self.id}, user_id={self.user_id}, provider={self.auth_provider})>"