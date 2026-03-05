from datetime import datetime, timezone
from uuid import UUID

from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.security import (
    JWT_ALGORITHM,
    JWT_REFRESH_SECRET_KEY,
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password as verify_password_hash,
)
from app.modules.auth.model import AuthCredential
from app.modules.user.model import User


class AuthService:
    def create_credentials(
        self,
        db: Session,
        user_id: UUID,
        password: str,
        auth_provider: str = "LOCAL",
    ) -> AuthCredential:
        credential = (
            db.query(AuthCredential)
            .filter(AuthCredential.user_id == user_id)
            .first()
        )

        if credential:
            credential.password_hash = hash_password(password)
            credential.password_algo = "bcrypt"
            credential.is_password_set = True
            credential.last_password_change = datetime.now(timezone.utc)
            credential.auth_provider = auth_provider
            db.add(credential)
            db.flush()
            db.refresh(credential)
            return credential

        credential = AuthCredential(
            user_id=user_id,
            auth_provider=auth_provider,
            password_hash=hash_password(password),
            password_algo="bcrypt",
            is_password_set=True,
            last_password_change=datetime.now(timezone.utc),
        )
        db.add(credential)
        db.flush()
        db.refresh(credential)
        return credential

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return verify_password_hash(plain_password, hashed_password)

    def generate_tokens(self, user: User) -> dict[str, str]:
        claims = {
            "sub": str(user.id),
            "tenant_id": str(user.tenant_id),
            "email": user.email,
            "role_id": str(user.role_id) if user.role_id else None,
        }
        access_token = create_access_token(claims)
        refresh_token = create_refresh_token(claims)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def refresh_access_token(self, refresh_token: str) -> str:
        try:
            payload = jwt.decode(
                refresh_token,
                JWT_REFRESH_SECRET_KEY,
                algorithms=[JWT_ALGORITHM],
            )
        except JWTError as exc:
            raise ValueError("Invalid refresh token") from exc

        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")

        claims = {
            "sub": payload.get("sub"),
            "tenant_id": payload.get("tenant_id"),
            "email": payload.get("email"),
            "role_id": payload.get("role_id"),
        }

        if not claims["sub"] or not claims["tenant_id"]:
            raise ValueError("Invalid refresh token payload")

        return create_access_token(claims)
