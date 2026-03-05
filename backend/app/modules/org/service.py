class OrganizationService:
    def create_organization(self, name: str):
        print("Creating organization with name:", name)
        return {"id": 2, "name": name}
    
    def get_organization(self, org_id: int):
        print("Fetching organization with id:", org_id)
        return {"id": org_id, "name": "Sample Org"}


