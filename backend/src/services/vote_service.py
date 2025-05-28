"""
Vote Service Module.

This module provides services for managing vote entities,
including CRUD operations and retrieving votes by user or form.
A vote represents a student's preference for other students in a form.
"""

from flask import request, current_app
from models.vote import Vote
from extensions import db
from services.utils import ensure_app_context

class VoteService:
    """
    Service class for handling vote-related operations.
    
    This class provides methods for vote management including creating,
    retrieving, and deleting vote records, as well as retrieving votes
    by user or form.
    """
    
    @staticmethod
    @ensure_app_context
    def get_all_votes():
        """
        Retrieves all votes from the database.
        
        Returns:
            list: A list of dictionaries containing vote information
        """
        votes = Vote.query.all()
        return [vote.to_dict() for vote in votes]
    
    @staticmethod
    @ensure_app_context
    def get_votes_by_user(user_id):
        """
        Retrieves all votes made by a specific user.
        
        Args:
            user_id (int): The ID of the user who made the votes
            
        Returns:
            list: A list of dictionaries containing the user's votes
        """
        votes = Vote.query.filter_by(vote_userid=user_id).all()
        return [vote.to_dict() for vote in votes]
    
    @staticmethod
    @ensure_app_context
    def get_votes_by_form(form_id):
        """
        Retrieves all votes for a specific form.
        
        Args:
            form_id (int): The ID of the form
            
        Returns:
            list: A list of dictionaries containing votes for the form
        """
        votes = Vote.query.filter_by(vote_formid=form_id).all()
        return [vote.to_dict() for vote in votes]
        
    @staticmethod
    def create_vote():
        """
        Creates a new vote based on the request data.
        
        Expects a JSON body with 'userid', 'idform', 'idstudent',
        and 'weight' fields.
        
        Returns:
            tuple: A tuple containing (response_data, status_code)
            - response_data is either the new vote data or an error message
            - status_code is the HTTP status code (201 for success)
            
        Raises:
            Exception: If database operations fail
        """
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
    @ensure_app_context
    def get_vote(vote_id):
        """
        Retrieves a vote by ID.
        
        Args:
            vote_id (int): The ID of the vote to retrieve
            
        Returns:
            dict: The vote data if found, None otherwise
        """
        vote = Vote.query.get(vote_id)
        if vote:
            return vote.to_dict()
        return None
    
    @staticmethod
    @ensure_app_context
    def delete_vote(vote_id):
        """
        Deletes a vote by ID.
        
        Args:
            vote_id (int): The ID of the vote to delete
            
        Returns:
            tuple: A tuple containing (response_data, status_code)
            - response_data is a success or error message
            - status_code is the HTTP status code (204 for success, 404 if not found)
            
        Raises:
            Exception: If database operations fail
        """
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
