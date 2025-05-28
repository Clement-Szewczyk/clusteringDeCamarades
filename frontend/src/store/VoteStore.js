import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiCluster from '../../api/api';

export const useVoteStore = defineStore('vote', () => {
    // State
    const votes = ref([]);
    const loading = ref(false);
    const error = ref(null);
    
    // Actions
    
    // Récupérer tous les votes
    async function fetchAllVotes() {
        try {
            loading.value = true;
            const response = await apiCluster.get('votes');
            console.log('All votes:', response.data);
            votes.value = response.data;
            return votes.value;
        } catch (err) {
            console.error('Error fetching votes:', err);
            error.value = err.message || 'Erreur lors de la récupération des votes';
            throw err;
        } finally {
            loading.value = false;
        }
    }
    
    // Récupérer les votes d'un utilisateur spécifique
    async function fetchUserVotes(userId) {
        try {
            loading.value = true;
            const response = await apiCluster.get(`users/${userId}/votes`);
            console.log(`Votes for user ${userId}:`, response.data);
            votes.value = response.data;
            return votes.value;
        } catch (err) {
            console.error(`Error fetching votes for user ${userId}:`, err);
            error.value = err.message || 'Erreur lors de la récupération des votes';
            throw err;
        } finally {
            loading.value = false;
        }
    }
    
    // Récupérer les votes pour un formulaire spécifique
    async function fetchFormularVotes(formularId) {
        try {
            loading.value = true;
            const response = await apiCluster.get(`formulars/${formularId}/votes`);
            console.log(`Votes for formular ${formularId}:`, response.data);
            votes.value = response.data;
            return votes.value;
        } catch (err) {
            console.error(`Error fetching votes for formular ${formularId}:`, err);
            error.value = err.message || 'Erreur lors de la récupération des votes';
            throw err;
        } finally {
            loading.value = false;
        }
    }
    
    // Créer un vote
    async function createVote(voteData) {
        try {
            loading.value = true;
            
            const response = await apiCluster.post('votes', {
                userid: voteData.userid,
                idform: voteData.idform,
                idstudent: voteData.idstudent,
                weight: voteData.weight
            });
            
            console.log('Vote created:', response.data);
            return response.data;
        } catch (err) {
            console.error('Error creating vote:', err);
            error.value = err.message || 'Erreur lors de la création du vote';
            throw err;
        } finally {
            loading.value = false;
        }
    }
    
    // Soumettre plusieurs votes en une fois (pour le formulaire de points)
    async function submitVotes(formularId, userId, votesData) {
        try {
            loading.value = true;
            const promises = votesData.map(vote => {
                return createVote({
                    userid: userId,
                    idform: formularId,
                    idstudent: vote.student_id,
                    weight: vote.points
                });
            });
            
            const results = await Promise.all(promises);
            console.log('All votes submitted successfully:', results);
            return results;
        } catch (err) {
            console.error('Error submitting votes:', err);
            error.value = err.message || 'Erreur lors de la soumission des votes';
            throw err;
        } finally {
            loading.value = false;
        }
    }
    
    // Supprimer un vote
    async function deleteVote(voteId) {
        try {
            loading.value = true;
            await apiCluster.delete(`votes/${voteId}`);
            console.log(`Vote ${voteId} deleted successfully`);
            return true;
        } catch (err) {
            console.error(`Error deleting vote ${voteId}:`, err);
            error.value = err.message || 'Erreur lors de la suppression du vote';
            throw err;
        } finally {
            loading.value = false;
        }
    }
    
    return {
        votes,
        loading,
        error,
        fetchAllVotes,
        fetchUserVotes,
        fetchFormularVotes,
        createVote,
        submitVotes,
        deleteVote
    };
});