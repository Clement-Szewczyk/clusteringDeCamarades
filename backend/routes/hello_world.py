from flask_restful import Resource
from services.hello_world_service import HelloWorldService

class HelloWorld(Resource):
    def get(self):
        """Handle GET requests to return a hello world message."""
        return HelloWorldService.get_hello_world()
    
def registerHelloWorldRoutes(api):
    api.add_resource(HelloWorld, '/hello')