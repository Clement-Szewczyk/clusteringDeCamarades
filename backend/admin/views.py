from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))

class StudentModelView(SecureModelView):
    column_searchable_list = ['name', 'email']
    column_filters = ['year', 'group']
    column_exclude_list = ['password_hash']
    can_export = True

class UserModelView(SecureModelView):
    column_exclude_list = ['password_hash']
    column_searchable_list = ['username', 'email']
    can_export = True

class FormularModelView(SecureModelView):
    column_searchable_list = ['title']
    column_filters = ['created_date']
    can_export = True

class RoleModelView(SecureModelView):
    column_searchable_list = ['name']

class TeacherModelView(SecureModelView):
    column_searchable_list = ['name', 'email']

class VoteModelView(SecureModelView):
    column_filters = ['created_date']
