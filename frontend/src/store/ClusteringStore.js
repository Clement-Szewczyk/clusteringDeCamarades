import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiCluster from '../../api/api';

export const useClusteringStore = defineStore('clustering', () => {
    // State
    const clusteringResults = ref(null);
    const loading = ref(false);
    const error = ref(null);
    
    // Actions
    async function generateClusters(formularId) {
        try {
            loading.value = true;
            error.value = null;
            console.log(`Generating clusters for formular ${formularId}...`);
            
            const response = await apiCluster.post(`clustering/${formularId}/generate`);
            console.log('Clustering results:', response.data);
            clusteringResults.value = response.data;
            return response.data;
        } catch (err) {
            console.error('Error generating clusters:', err);
            error.value = err.message || 'Une erreur est survenue lors de la génération des clusters';
            throw err;
        } finally {
            loading.value = false;
        }
    }
    
    async function fetchClusteringResults(formularId) {
        try {
            loading.value = true;
            error.value = null;
            console.log(`Fetching clusters for formular ${formularId}...`);
            
            const response = await apiCluster.get(`clustering/${formularId}`);
            console.log('Clustering results fetched:', response.data);
            clusteringResults.value = response.data;
            return response.data;
        } catch (err) {
            console.error('Error fetching clustering results:', err);
            error.value = err.message || 'Une erreur est survenue lors de la récupération des clusters';
            throw err;
        } finally {
            loading.value = false;
        }
    }
    
    function clearResults() {
        clusteringResults.value = null;
        error.value = null;
    }
    
    return {
        clusteringResults,
        loading,
        error,
        generateClusters,
        fetchClusteringResults,
        clearResults
    };
});