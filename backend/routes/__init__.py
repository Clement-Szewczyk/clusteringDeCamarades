# Routes package initialization
# This file allows the routes directory to be treated as a package

from .hello_world import registerHelloWorldRoutes
from .student import registerStudentRoutes


def register_routes(app, api):
    """Register all API routes"""
    registerHelloWorldRoutes(api)
    registerStudentRoutes(api)


