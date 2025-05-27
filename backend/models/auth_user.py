from extensions import db

class AuthUser(db.Model):
    __tablename__ = 'auth_user'
    
    auth_user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auth_user_email = db.Column(db.String(255), nullable=False)
    auth_user_mdp = db.Column(db.String(255), nullable=False)
    auth_user_name = db.Column(db.String(100), nullable=False)
    auth_user_firstname = db.Column(db.String(100), nullable=False)
    
    # Relationships
    roles = db.relationship('UserRole', backref='user', lazy=True)
    formulars = db.relationship('Formular', backref='creator', lazy=True)
    votes = db.relationship('Vote', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<AuthUser {self.auth_user_email}>'
    
    def to_dict(self):
        return {
            'auth_user_id': self.auth_user_id,
            'auth_user_email': self.auth_user_email,
            'auth_user_name': self.auth_user_name,
            'auth_user_firstname': self.auth_user_firstname
        }
