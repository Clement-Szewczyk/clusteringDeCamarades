from extensions import db

class Role(db.Model):
    __tablename__ = 'role'
    
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(15), nullable=False)
    
    # Relationships
    users = db.relationship('UserRole', backref='role', lazy=True)
    
    def __repr__(self):
        return f'<Role {self.role_name}>'
    
    def to_dict(self):
        return {
            'role_id': self.role_id,
            'role_name': self.role_name
        }
