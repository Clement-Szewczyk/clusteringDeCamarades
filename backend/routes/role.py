from flask_restful import Resource
from services.role_service import RoleService

class RoleResource(Resource):
    def get(self, role_id=None):
        """
        Retrieves a role by ID, or all roles if no ID is specified.
        """
        if role_id:
            role = RoleService.get_role(role_id)
            if role:
                return role
            return {'error': 'Role not found'}, 404
        else:
            return RoleService.get_all_roles()
    
    def post(self):
        """
        Create a new role.
        """
        return RoleService.create_role()
    

def registerRoleRoutes(api):
    api.add_resource(RoleResource, '/roles', '/roles/<int:role_id>')