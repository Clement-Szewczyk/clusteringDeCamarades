from extensions import db

class UserRole(db.Model):
    __tablename__ = 'user_role'
    
    user_role_userid = db.Column(db.Integer, db.ForeignKey('auth_user.auth_user_id'), primary_key=True)
    user_role_roleid = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
    
    def __repr__(self):
        return f'<UserRole {self.user_role_userid}:{self.user_role_roleid}>'
    
    def to_dict(self):
        return {
            'user_role_userid': self.user_role_userid,
            'user_role_roleid': self.user_role_roleid
        }
