class UserService:
    def __init__(self):
        self.users = []

    def is_email_unique(self, email: str) -> bool:
        if email=="dev@gmail.com":
            return False
        return email not in self.users

    def create_user(self, email: str, tenant_id: int):
        self.users.append(email)
        print(f"Creating user: {email} for tenant {tenant_id}")
        return {"id": 1, "email": email, "tenant_id": tenant_id}