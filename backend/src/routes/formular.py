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
            return FormularService.get_all_formular()
    
    def post(self):
        """
        Create a new formular.
        """
        print("TOTOOOOOOOOOOOOOOOOOOOOOO")
        return FormularService.create_formular()
    
    def put(self, formular_id):
        """
        Updates an existing formular.
        """
        return FormularService.update_formular(formular_id)
    
    def delete(self, formular_id):
        """
        Deletes a formular by ID.
        """
        return FormularService.delete_formular(formular_id)

class TeacherFormularResource(Resource):
    def get(self, teacher_id):
        """
        Retrieves all formulars created by a specific teacher.
        """
        return FormularService.get_all_teacher_formular(teacher_id)

def registerFormularRoutes(api):
    api.add_resource(FormularResource, '/formulars', '/formulars/<int:formular_id>')
    api.add_resource(TeacherFormularResource, '/teachers/<int:teacher_id>/formulars')
