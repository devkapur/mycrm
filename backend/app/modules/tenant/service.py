from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.tenant.model import Tenant
from app.modules.tenant.schema import TenantCreate, TenantUpdate


class TenantService:
    def create_tenant(self, db: Session, payload: TenantCreate) -> Tenant:
        tenant = Tenant(**payload.model_dump(exclude_none=True))
        db.add(tenant)
        db.flush()
        return tenant

    def get_tenant_by_id(self, db: Session, tenant_id: UUID) -> Tenant | None:
        return (
            db.query(Tenant)
            .filter(Tenant.id == tenant_id, Tenant.deleted_at.is_(None))
            .first()
        )

    def get_tenant_by_domain(self, db: Session, domain: str) -> Tenant | None:
        return (
            db.query(Tenant)
            .filter(Tenant.domain == domain, Tenant.deleted_at.is_(None))
            .first()
        )

    def update_tenant(self, db: Session, tenant: Tenant, payload: TenantUpdate) -> Tenant:
        update_data = payload.model_dump(exclude_none=True)
        for field, value in update_data.items():
            setattr(tenant, field, value)

        db.add(tenant)
        db.flush()
        db.refresh(tenant)
        return tenant