from flask_restful import Resource
from services.auth_service import AuthService

class AuthRegister(Resource):
    def post(self):
        """Handle registration requests"""
        return AuthService.register()

class AuthLogin(Resource):
    def post(self):
        """Handle login requests"""
        return AuthService.login()

def registerAuthRoutes(api):
    api.add_resource(AuthRegister, '/auth/register')
    api.add_resource(AuthLogin, '/auth/login')