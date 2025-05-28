from flask_restful import Resource
from services.clustering_service import ClusteringService

class ClusteringResource(Resource):
    def get(self, formular_id):
        """
        Generate student clusters based on votes for a specific formular.
        
        Args:
            formular_id (int): The ID of the formular to generate groups for
            
        Returns:
            JSON: Groups of students and satisfaction metrics
        """
        return ClusteringService.get_clustering_for_formular(formular_id)

def registerClusteringRoutes(api):
    api.add_resource(ClusteringResource, '/clustering/<int:formular_id>')
