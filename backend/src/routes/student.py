from flask_restful import Resource, request
from services.student_service import StudentService

class StudentResource(Resource):
    def get(self, student_id=None):
        """
        Retrieves a student by ID, or all students if no ID is specified.
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
        Create a new student.
        """
        return StudentService.create_student()
    
    def put(self, student_id):
        """
        Updates an existing student with its ID.
        """
        return StudentService.update_student(student_id)
    
    def delete(self, student_id):
        """
        Deletes a student by ID.
        """
        return StudentService.delete_student(student_id)

class StudentBatchResource(Resource):
    def post(self):
        """
        Creates several students in a single request.
        """
        return StudentService.create_students_batch()

def registerStudentRoutes(api):
    api.add_resource(StudentResource, '/students', '/students/<int:student_id>')
    api.add_resource(StudentBatchResource, '/students/batch')
