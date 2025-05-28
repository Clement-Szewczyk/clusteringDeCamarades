from flask import request, current_app
from models.vote import Vote
from extensions import db

class VoteService:
    @staticmethod
    def _ensure_app_context(func):
        """Decorator to ensure database operations run in an app context"""
        def wrapper(*args, **kwargs):
            try:
                # Check if we're already in an app context
                current_app._get_current_object()
                return func(*args, **kwargs)
            except RuntimeError:
                # If not, get the app and create a context
                from app import get_app
                app = get_app()
                with app.app_context():
                    return func(*args, **kwargs)
        return wrapper
    
    @staticmethod
    @_ensure_app_context
    def get_all_votes():
        """Retrieves all votes"""
        votes = Vote.query.all()
        return [vote.to_dict() for vote in votes]
    
    @staticmethod
    @_ensure_app_context
    def get_votes_by_user(user_id):
        """Retrieves all votes made by a specific user"""
        votes = Vote.query.filter_by(vote_userid=user_id).all()
        return [vote.to_dict() for vote in votes]
    
    @staticmethod
    @_ensure_app_context
    def get_votes_by_form(form_id):
        """Retrieves all votes for a specific form"""
        votes = Vote.query.filter_by(vote_formid=form_id).all()
        return [vote.to_dict() for vote in votes]
        
    @staticmethod
    def create_vote():
        """Creates a new vote"""
        data = request.get_json()
        
        if not data:
            return {'error': 'No data provided'}, 400
            
        required_fields = ['userid', 'idform', 'idstudent', 'weight']
        for field in required_fields:
            if field not in data:
                return {'error': f'Missing required field: {field}'}, 400
        
        try:
            new_vote = Vote(
                vote_userid=data['userid'],
                vote_formid=data['idform'],
                vote_studentid=data['idstudent'],
                weigth=data['weight']
            )
            
            db.session.add(new_vote)
            db.session.commit()
            return new_vote.to_dict(), 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create vote: {str(e)}'}, 500
    
    @staticmethod
    @_ensure_app_context
    def get_vote(vote_id):
        """Retrieves a vote by ID"""
        vote = Vote.query.get(vote_id)
        if vote:
            return vote.to_dict()
        return None
    
    @staticmethod
    @_ensure_app_context
    def delete_vote(vote_id):
        """Deletes a vote by ID"""
        vote = Vote.query.get(vote_id)
        if not vote:
            return {'error': 'Vote not found'}, 404
        
        try:
            db.session.delete(vote)
            db.session.commit()
            return {'message': 'Vote deleted successfully'}, 204
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to delete vote: {str(e)}'}, 500
