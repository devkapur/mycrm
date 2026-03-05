from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.user.model import User, UserStatus
from app.modules.user.schema import UserCreate, UserUpdate


class UserService:
    def check_email_available(self, db: Session, tenant_id: UUID, email: str) -> bool:
        user_exists = (
            db.query(User.id)
            .filter(
                User.tenant_id == tenant_id,
                func.lower(User.email) == email.lower(),
                User.deleted_at.is_(None),
            )
            .first()
            is not None
        )
        return not user_exists
    

    def check_email_globally_available(self, db: Session, email: str) -> bool:
        user_exists = (
        db.query(User.id)
        .filter(
            func.lower(User.email) == email.lower(),
            User.deleted_at.is_(None),
            
        )
        .first()
        is not None
        )
        return not user_exists


    def create_user(
        self,
        db: Session,
        tenant_id: UUID,
        payload: UserCreate,
        role_id: UUID | None = None,
        profile_id: UUID | None = None,
        status: UserStatus = UserStatus.active,
    ) -> User:
        
        if not self.check_email_available(db, tenant_id, payload.email):
            raise ValueError(f"Email {payload.email} already exists in this tenant")

        user = User(
            tenant_id=tenant_id,
            email=payload.email.lower(),
            first_name=payload.first_name,
            last_name=payload.last_name,
            role_id=role_id,
            profile_id=profile_id,
            status=status,
        )
        db.add(user)
        db.flush()
        db.refresh(user)
        return user

    def get_user_by_email(self, db: Session, tenant_id: UUID, email: str) -> User | None:
        return (
            db.query(User)
            .filter(
                User.tenant_id == tenant_id,
                func.lower(User.email) == email.lower(),
                User.deleted_at.is_(None),
            )
            .first()
        )

    def get_user_by_id(self, db: Session, tenant_id: UUID, user_id: UUID) -> User | None:
        return (
            db.query(User)
            .filter(
                User.id == user_id,
                User.tenant_id == tenant_id,
                User.deleted_at.is_(None),
            )
            .first()
        )

    def update_user(
        self,
        db: Session,
        tenant_id: UUID,
        user_id: UUID,
        payload: UserUpdate,
    ) -> User | None:
        user = self.get_user_by_id(db=db, tenant_id=tenant_id, user_id=user_id)
        if not user:
            return None

        update_data = payload.model_dump(exclude_none=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        db.add(user)
        db.flush()
        db.refresh(user)
        return user



