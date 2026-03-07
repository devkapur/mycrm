import re
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import exists, func
from app.modules.role.model import Role
from app.modules.role.schema import RoleCreate, RoleUpdate



class RoleService:

    def _generate_slug(self, name: str) -> str:
        return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    
    def would_create_cycle(self, db: Session, tenant_id: UUID, role_id: UUID, new_parent_id: UUID):
        if role_id is None:
            return False
        
        current = new_parent_id

        while current:
            if current == role_id:
                return True

            role = self.get_role_by_id(db, tenant_id, current)
            current = role.reporting_to if role else None

        return False

    def create_role(self, db: Session, tenant_id: UUID, payload: RoleCreate) -> Role:
        slug = self._generate_slug(payload.name)

        existing = self.get_role_by_slug(db, tenant_id, slug)
        if existing:
            raise ValueError("Role slug already exists")

        if payload.reporting_to:
            if self.would_create_cycle(db, tenant_id, None, payload.reporting_to):
                raise ValueError("Role hierarchy cycle detected")


        role = Role(
            tenant_id=tenant_id,
            name=payload.name,
            slug=slug,
            description=payload.description,
            reporting_to=payload.reporting_to,
            level=payload.level,
            data_scope=payload.data_scope,
            share_with_peers=payload.share_with_peers
        )
        db.add(role)
        db.flush()
        db.refresh(role)
        return role
    
    def update_role(self, db: Session, tenant_id: UUID, role_id: UUID, payload: RoleUpdate) -> Role | None:
        role = self.get_role_by_id(db, tenant_id, role_id)
        if not role:
            return None
        
        update_data = payload.model_dump(exclude_none=True)

        if "name" in update_data:
            new_slug = self._generate_slug(update_data["name"])

            existing = self.get_role_by_slug(db, tenant_id, new_slug)
            if existing and existing.id != role.id:
                raise ValueError("Role slug already exists")

            update_data["slug"] = new_slug

        if "reporting_to" in update_data:
            new_parent = update_data["reporting_to"]

            if new_parent == role.id:
                raise ValueError("Role cannot report to itself")
            
            if self.would_create_cycle(db, tenant_id, role.id, new_parent):
                raise ValueError("Role hierarchy cycle detected")

        for field, value in update_data.items():
            setattr(role, field, value)

        db.flush()
        db.refresh(role)
        return role

    def get_role_by_id(self, db: Session, tenant_id: UUID, role_id: UUID) -> Role | None:
        return (
            db.query(Role)
            .filter(
                Role.id == role_id,
                Role.tenant_id == tenant_id,
                Role.deleted_at.is_(None)
            )
            .first()
        )
    def get_role_by_slug(self, db: Session, tenant_id: UUID, slug: str) -> Role | None:
        return (
            db.query(Role)
            .filter(
                Role.slug == slug,
                Role.tenant_id == tenant_id,
                Role.deleted_at.is_(None)
            )
            .first()
        )
    def list_roles(self, db: Session, tenant_id: UUID):
        return (
            db.query(Role)
            .filter(
                Role.tenant_id == tenant_id,
                Role.deleted_at.is_(None),
                Role.is_active == True
            )
            .order_by(Role.level.asc())
            .all()
        )

    def soft_delete_role(self, db: Session, tenant_id: UUID, role_id: UUID) -> bool:
        role = self.get_role_by_id(db, tenant_id, role_id)
        if not role:
            return False
       
        if role.is_system:
            raise ValueError("System roles cannot be deleted")

        from datetime import datetime, timezone
        role.deleted_at = datetime.now(timezone.utc)
        db.flush()
        return True
    
    def create_default_roles(self, db: Session, tenant_id: UUID) -> dict:
        ceo = self.create_role(
            db=db,
            tenant_id=tenant_id,
            payload=RoleCreate(
                name="CEO",
                level=1,
                reporting_to=None,
                data_scope="all",
                share_with_peers=False
            )
        )
        ceo.is_system = True
        ceo.is_default = True

        manager = self.create_role(
            db=db,
            tenant_id=tenant_id,
            payload=RoleCreate(
                name="Manager",
                level=2,
                reporting_to=ceo.id,
                data_scope="hierarchy"
            )
        )
        manager.is_default = True


        db.flush()

        return {
        "ceo": ceo,
        "manager": manager
        }