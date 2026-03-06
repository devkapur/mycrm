from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.modules.organization.model import Organization
from app.modules.organization.schema import OrganizationCreate, OrganizationUpdate


class OrganizationService:

    def create_organization(
        self,
        db: Session,
        tenant_id: UUID,
        payload: OrganizationCreate
    ) -> Organization:

        organization = Organization(
            tenant_id=tenant_id,
            company_name=payload.company_name,
            alias=payload.alias,
            phone=payload.phone,
            primary_email=payload.primary_email
        )

        db.add(organization)
        db.flush()
        db.refresh(organization)

        return organization


    def get_organization_by_id(
        self,
        db: Session,
        tenant_id: UUID,
        organization_id: UUID
    ) -> Organization | None:

        return (
            db.query(Organization)
            .filter(
                Organization.id == organization_id,
                Organization.tenant_id == tenant_id,
                Organization.deleted_at.is_(None)
            )
            .first()
        )


    def get_organization_by_tenant(
        self,
        db: Session,
        tenant_id: UUID
    ) -> Organization | None:

        return (
            db.query(Organization)
            .filter(
                Organization.tenant_id == tenant_id,
                Organization.deleted_at.is_(None)
            )
            .first()
        )


    def update_organization(
        self,
        db: Session,
        tenant_id: UUID,
        organization_id: UUID,
        payload: OrganizationUpdate
    ) -> Organization | None:

        organization = self.get_organization_by_id(
            db=db,
            tenant_id=tenant_id,
            organization_id=organization_id
        )

        if not organization:
            return None

        update_data = payload.model_dump(exclude_none=True)

        for field, value in update_data.items():
            setattr(organization, field, value)

        db.add(organization)
        db.flush()
        db.refresh(organization)

        return organization


    def deactivate_organization(
        self,
        db: Session,
        tenant_id: UUID,
        organization_id: UUID
    ) -> bool:

        organization = self.get_organization_by_id(
            db=db,
            tenant_id=tenant_id,
            organization_id=organization_id
        )

        if not organization:
            return False

        organization.is_active = False

        db.add(organization)
        db.flush()

        return True


    def soft_delete_organization(
        self,
        db: Session,
        tenant_id: UUID,
        organization_id: UUID
    ) -> bool:

        organization = self.get_organization_by_id(
            db=db,
            tenant_id=tenant_id,
            organization_id=organization_id
        )

        if not organization:
            return False

        organization.deleted_at = func.now()

        db.add(organization)
        db.flush()

        return True