from flask_restful import Resource
from services.vote_service import VoteService

class VoteResource(Resource):
    def get(self, vote_id=None):
        """
        Retrieves a vote by ID, or all votes if no ID is specified.
        """
        if vote_id:
            vote = VoteService.get_vote(vote_id)
            if vote:
                return vote
            return {'error': 'Vote not found'}, 404
        else:
            return VoteService.get_all_votes()
    
    def post(self):
        """
        Create a new vote.
        """
        return VoteService.create_vote()
    
    def delete(self, vote_id):
        """
        Deletes a vote by ID.
        """
        return VoteService.delete_vote(vote_id)

class UserVoteResource(Resource):
    def get(self, user_id):
        """
        Retrieves all votes made by a specific user.
        """
        return VoteService.get_votes_by_user(user_id)

class FormVoteResource(Resource):
    def get(self, form_id):
        """
        Retrieves all votes for a specific form.
        """
        return VoteService.get_votes_by_form(form_id)

def registerVoteRoutes(api):
    api.add_resource(VoteResource, '/votes', '/votes/<int:vote_id>')
    api.add_resource(UserVoteResource, '/users/<int:user_id>/votes')
    api.add_resource(FormVoteResource, '/formulars/<int:form_id>/votes')
