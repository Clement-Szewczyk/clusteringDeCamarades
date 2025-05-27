from extensions import db

class Vote(db.Model):
    __tablename__ = 'vote'
    
    vote_idvote = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vote_userid = db.Column(db.Integer, db.ForeignKey('auth_user.auth_user_id'), nullable=False)
    vote_formid = db.Column(db.Integer, db.ForeignKey('formular.formular_id'), nullable=False)
    vote_studentid = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    weigth = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<Vote {self.vote_idvote}>'
    
    def to_dict(self):
        return {
            'vote_idvote': self.vote_idvote,
            'vote_userid': self.vote_userid,
            'vote_formid': self.vote_formid,
            'vote_studentid': self.vote_studentid,
            'weigth': self.weigth
        }
