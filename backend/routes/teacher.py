from flask_restful import Resource, request
from services.teacher_service import TeacherService

class TeacherResource(Resource):
    def get(self, email=None):
        """
        Retrieves a teacher by email, or all teachers if no email is specified.
        """
        if email:
            teacher = TeacherService.get_teacher(email)
            if teacher:
                return teacher
            return {'error': 'Teacher not found'}, 404
        else:
            return TeacherService.get_all_teachers()
    
    def post(self):
        """
        Create a new teacher.
        """
        return TeacherService.create_teacher()
    
    def put(self, email):
        """
        Updates an existing teacher with its email.
        """
        return TeacherService.update_teacher(email)
    
    def delete(self, email):
        """
        Deletes a teacher by email.
        """
        return TeacherService.delete_teacher(email)

class TeacherBatchResource(Resource):
    def post(self):
        """
        Creates several teachers in a single request.
        """
        return TeacherService.create_teachers_batch()

def registerTeacherRoutes(api):
    api.add_resource(TeacherResource, '/teachers', '/teachers/<string:email>')
    api.add_resource(TeacherBatchResource, '/teachers/batch')
