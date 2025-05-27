from extensions import db

class Teacher(db.Model):
    __tablename__ = 'teacher'
    
    teacher_email = db.Column(db.String(255), primary_key=True)
    
    def __repr__(self):
        return f'<Teacher {self.teacher_email}>'
    
    def to_dict(self):
        return {
            'teacher_email': self.teacher_email
        }
