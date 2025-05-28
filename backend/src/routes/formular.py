from flask_restful import Resource
from services.formular_service import FormularService

class FormularResource(Resource):
    def get(self, formular_id=None):
        """
        Retrieves a formular by ID, or all formulars if no ID is specified.
        """
        if formular_id:
            formular = FormularService.get_formular(formular_id)
            if formular:
                return formular
            return {'error': 'Formular not found'}, 404
        else:
            return FormularService.get_all_formulars()
    
    def post(self):
        """
        Create a new formular.
        """
        return FormularService.create_formular()
    
    def put(self, formular_id):
        """
        Updates an existing formular.
        """
        return FormularService.update_formular(formular_id)
    
    def delete(self, formular_id):
        """
        Deletes a formular.
        """
        return FormularService.delete_formular(formular_id)

def registerFormularRoutes(api):
    api.add_resource(FormularResource, '/formulars', '/formulars/<int:formular_id>')
