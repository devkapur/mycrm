import re
from uuid import UUID
from sqlalchemy.orm import Session
from app.modules.profile.model import Profile
from app.modules.profile.schema import ProfileCreate, ProfileUpdate


class ProfileService:

    def _generate_slug(self, name: str) -> str:
        return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    
    def create_profile(self, db: Session, tenant_id: UUID, payload: ProfileCreate) -> Profile:
        slug = self._generate_slug(payload.name)

        existing = self.get_profile_by_slug(db, tenant_id, slug)
        if existing:        
            raise ValueError("Profile slug already exists") 
        
        profile = Profile(
            tenant_id=tenant_id,
            name=payload.name,
            slug=slug,
            description=payload.description,
            permissions=payload.permissions
        )
        db.add(profile)
        db.flush()
        db.refresh(profile)
        return profile
    
    def update_profile(self, db: Session, tenant_id: UUID, profile_id: UUID, payload: ProfileUpdate) -> Profile | None:
        profile = self.get_profile_by_id(db, tenant_id, profile_id)
        if not profile:
            return None
        
        update_data = payload.model_dump(exclude_none=True)

        if "name" in update_data:
            new_slug = self._generate_slug(update_data["name"])

            existing = self.get_profile_by_slug(db, tenant_id, new_slug)
            if existing and existing.id != profile.id:
                raise ValueError("Profile slug already exists")

            update_data["slug"] = new_slug
        for field, value in update_data.items():
            setattr(profile, field, value)

        db.flush()
        db.refresh(profile)
        return profile

    def get_profile_by_id(self, db: Session, tenant_id: UUID, profile_id: UUID) -> Profile | None:
        return (
            db.query(Profile)
            .filter(
                Profile.id == profile_id,
                Profile.tenant_id == tenant_id,
                Profile.deleted_at.is_(None)
            )
            .first()
        )
    def get_profile_by_slug(self, db: Session, tenant_id: UUID, slug: str) -> Profile | None:
        return (
            db.query(Profile)
            .filter(
                Profile.slug == slug,
                Profile.tenant_id == tenant_id,
                Profile.deleted_at.is_(None)
            )
            .first()
        )

    def list_profiles(self, db: Session, tenant_id: UUID):
        return (
            db.query(Profile)
            .filter(
                Profile.tenant_id == tenant_id,
                Profile.deleted_at.is_(None),
                Profile.is_active == True
            )
            .order_by(Profile.created_at.desc())
            .all()
        )

    def soft_delete_profile(self, db: Session, tenant_id: UUID, profile_id: UUID) -> bool:
        profile = self.get_profile_by_id(db, tenant_id, profile_id)
        if not profile:
            return False
        
        if profile.is_system:
            raise ValueError("System profiles cannot be deleted")

        from datetime import datetime, timezone
        profile.deleted_at = datetime.now(timezone.utc)
        db.flush()
        return True
    
    def create_default_profiles(self, db: Session, tenant_id: UUID) -> dict:
        admin = self.create_profile(
            db=db,
            tenant_id=tenant_id,
            payload=ProfileCreate(
                name="Administrator",
                description="Administrator profile",
                permissions={
                    "users":    ["view", "create", "edit", "delete"],
                    "roles":    ["view", "create", "edit", "delete"],
                    "profiles": ["view", "create", "edit", "delete"],
                    "org":      ["view", "edit"]

                }
            )
        )
        admin.is_system = True
        admin.is_default = True

        employee = self.create_profile(
            db=db,
            tenant_id=tenant_id,
            payload=ProfileCreate(
                name="Employee",
                description="Employee profile",
                permissions={
                    "users": ["view"],
                    "roles": ["view"],
                    "profiles": ["view"],
                    "org": ["view"]     
                    }
                ) 
        )
        employee.is_default = True

        db.flush()

        return {
            "admin": admin,
            "employee": employee
            }     