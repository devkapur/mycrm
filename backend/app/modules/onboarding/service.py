from app.modules.org.service import OrganizationService
from app.modules.user.service import UserService

class OnboardingService:
    def __init__(self, organization_service: OrganizationService, user_service: UserService):
        self.organization_service = organization_service
        self.user_service = user_service

    def register_company(self, name: str, email: str):

        # 1. Email uniqueness check
        if not self.user_service.is_email_unique(email):
            raise ValueError("Email already exists")

        # 2. Create organization
        org = self.organization_service.create_organization(name)

        # 3. Create user
        user = self.user_service.create_user(email, tenant_id=org["id"])

        # 4. Return response
        return {
            "organization": org,
            "owner": user
        }



org_service = OrganizationService()
user_service = UserService()

onboarding = OnboardingService(org_service, user_service)

result = onboarding.register_company("Dev CRM", "dev1@gmail.com")

print(result)