from flask_restful import Resource, request
from services.student_service import StudentService

class StudentResource(Resource):
    def get(self, student_id=None):
        """
        Récupère un étudiant par son ID ou tous les étudiants si aucun ID n'est spécifié.
        """
        if student_id:
            student = StudentService.get_student(student_id)
            if student:
                return student
            return {'error': 'Student not found'}, 404
        else:
            return StudentService.get_all_students()
    
    def post(self):
        """
        Crée un nouvel étudiant.
        """
        return StudentService.create_student()
    
    def put(self, student_id):
        """
        Met à jour un étudiant existant par son ID.
        """
        return StudentService.update_student(student_id)
    
    def delete(self, student_id):
        """
        Supprime un étudiant par son ID.
        """
        return StudentService.delete_student(student_id)

class StudentBatchResource(Resource):
    def post(self):
        """
        Crée plusieurs étudiants en une seule requête.
        """
        return StudentService.create_students_batch()

def registerStudentRoutes(api):
    api.add_resource(StudentResource, '/students', '/students/<int:student_id>')
    api.add_resource(StudentBatchResource, '/students/batch')
