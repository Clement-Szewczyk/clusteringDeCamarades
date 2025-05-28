from extensions import db
from datetime import datetime

class Formular(db.Model):
    __tablename__ = 'formular'
    
    formular_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    formular_title = db.Column(db.String(100), nullable=False)
    formular_description = db.Column(db.Text, nullable=False)
    formular_creator = db.Column(db.Integer, db.ForeignKey('auth_user.auth_user_id'), nullable=False)
    formular_start = db.Column(db.DateTime, nullable=False)
    formular_end = db.Column(db.DateTime, nullable=False)
    formular_nb_vote_per_person = db.Column(db.Integer, nullable=False)
    
    # Relationships
    votes = db.relationship('Vote', backref='formular', lazy=True)
    
    def __repr__(self):
        return f'<Formular {self.formular_title}>'
    
    def to_dict(self):
        return {
            'formular_id': self.formular_id,
            'formular_title': self.formular_title,
            'formular_description': self.formular_description,
            'formular_creator': self.formular_creator,
            'formular_start': self.formular_start.isoformat(),
            'formular_end': self.formular_end.isoformat(),
            'formular_nb_person_group': self.formular_nb_vote_per_person
        }
