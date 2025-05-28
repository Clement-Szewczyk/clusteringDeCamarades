"""
Routes Package Initialization.

This package organizes and registers all API routes for the application.
It imports and consolidates route registration functions from individual route modules
and provides a centralized function for registering all routes with the Flask application.
"""

from .hello_world import registerHelloWorldRoutes
from .student import registerStudentRoutes
from .teacher import registerTeacherRoutes
from .auth import registerAuthRoutes
from .role import registerRoleRoutes
from .formular import registerFormularRoutes
from .vote import registerVoteRoutes

def register_routes(app, api):
    """
    Register all API routes with the Flask application.
    
    This function calls the registration function from each route module
    to add all API endpoints to the provided Flask-RESTful API instance.
    
    Args:
        app (Flask): The Flask application instance
        api (Api): The Flask-RESTful API instance
    """
    registerHelloWorldRoutes(api)
    registerStudentRoutes(api)
    registerTeacherRoutes(api)
    registerAuthRoutes(api)
    registerRoleRoutes(api)
    registerFormularRoutes(api)
    registerVoteRoutes(api)

