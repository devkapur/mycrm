from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, create_refresh_token, hash_password
from app.modules.auth.model import AuthCredential
from app.modules.onboarding.schema import OnboardingRequestDTO, OnboardingResponseDTO
from app.modules.org.organization_model import Organization
from app.modules.profile.model import Profile
from app.modules.role.model import Role
from app.modules.tenant.model import Tenant
from app.modules.user.model import User, UserStatus


class OnboardingService:
    def validate_email(self, db: Session, email: str) -> None:
        email_exists = (
            db.query(User.id)
            .filter(func.lower(User.email) == email.lower(), User.deleted_at.is_(None))
            .first()
            is not None
        )
        if email_exists:
            raise ValueError("User already exists")

    def register_company(self, db: Session, payload: OnboardingRequestDTO) -> OnboardingResponseDTO:
        # 1) Validate email
        self.validate_email(db, payload.email)

        try:
            # 2) Start transaction
            with db.begin():
                # 3) Create tenant
                tenant = Tenant(name=payload.company_name, domain=payload.domain)
                db.add(tenant)
                db.flush()

                organization = Organization(
                    tenant_id=tenant.id,
                    company_name=payload.company_name,
                    primary_email=payload.email,
                )
                db.add(organization)

                # 4) Get owner role
                owner_role = self._get_or_create_owner_role(db, tenant_id=tenant.id)

                # 7) Seed default data
                default_profile = self._seed_default_data(db, tenant_id=tenant.id)

                # 5) Create user
                user = User(
                    tenant_id=tenant.id,
                    email=payload.email.lower(),
                    first_name=payload.first_name,
                    last_name=payload.last_name,
                    role_id=owner_role.id,
                    profile_id=default_profile.id,
                    status=UserStatus.active,
                )
                db.add(user)
                db.flush()

                # 6) Create auth credentials
                auth_credential = AuthCredential(
                    user_id=user.id,
                    auth_provider="LOCAL",
                    password_hash=hash_password(payload.password),
                    password_algo="bcrypt",
                    is_password_set=True,
                    last_password_change=datetime.now(timezone.utc),
                )
                db.add(auth_credential)

            # 8) Commit is handled by context manager
        except IntegrityError as exc:
            db.rollback()
            raise ValueError("Unable to complete onboarding due to data conflict") from exc

        # 9) Generate tokens
        claims = {
            "sub": str(user.id),
            "tenant_id": str(tenant.id),
            "email": user.email,
            "role": owner_role.slug,
        }
        access_token = create_access_token(claims)
        refresh_token = create_refresh_token(claims)

        # 10) Return response DTO
        return OnboardingResponseDTO(
            tenant_id=tenant.id,
            organization_id=organization.id,
            user_id=user.id,
            role_id=owner_role.id,
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def _get_or_create_owner_role(self, db: Session, tenant_id):
        owner_role = (
            db.query(Role)
            .filter(
                Role.tenant_id == tenant_id,
                func.lower(Role.slug) == "owner",
                Role.deleted_at.is_(None),
            )
            .first()
        )

        if owner_role:
            return owner_role

        owner_role = Role(
            tenant_id=tenant_id,
            name="Owner",
            slug="owner",
            description="Tenant owner with full access",
            level=1,
            data_scope="all",
            is_system=True,
            is_default=True,
            is_active=True,
            share_with_peers=False,
        )
        db.add(owner_role)
        db.flush()
        return owner_role

    def _seed_default_data(self, db: Session, tenant_id):
        default_profile = (
            db.query(Profile)
            .filter(
                Profile.tenant_id == tenant_id,
                func.lower(Profile.slug) == "default",
                Profile.deleted_at.is_(None),
            )
            .first()
        )

        if default_profile:
            return default_profile

        default_profile = Profile(
            tenant_id=tenant_id,
            name="Default",
            slug="default",
            description="Default profile for initial onboarding",
            permissions={},
            is_system=True,
            is_default=True,
            is_active=True,
            settings={},
        )
        db.add(default_profile)
        db.flush()
        return default_profile
