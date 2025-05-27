from extensions import db

class Student(db.Model):
    """Student model representing the student table"""
    __tablename__ = 'student'
    
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_email = db.Column(db.String(255), unique=True, nullable=False)
    
    # Relationship with Vote model
    votes = db.relationship('Vote', backref='student', lazy=True)
    
    def __repr__(self):
        return f"<Student {self.student_email}>"
    
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'student_email': self.student_email
        }
