from flask import request

class HelloWorldService:
    @staticmethod
    def get_hello_world():
        # Retourne un message de salutation
        return {'message': 'Hello, World!'}

    @staticmethod
    def create_hello_world():
        # Crée un message de salutation basé sur les données fournies
        data = request.get_json()
        message = data.get('message', 'Hello, World!')
        return {'message': message}, 201