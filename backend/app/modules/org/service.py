class OrganizationService:
    def create_organization(self, name: str):
        print("Creating organization with name:", name)
        return {"id": 1, "name": name}
         