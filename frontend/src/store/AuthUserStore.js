import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiCluster from '../../api/api';

export const useAuthUserStore = defineStore('user', () => {
    // State
    const user = ref(null);
    
    // Actions
async function signup(email, password, nom, prenom) {
    try {
        console.log("Trying to add user", { email, password, nom, prenom });
        const response = await apiCluster.post('auth/register', { 
            email: email,
            password: password,
            nom: nom,
            prenom: prenom
        });
        console.log('User added:', response.data);
        user.value = response.data;
        return response.data;
    } catch (error) {
        console.error("Error adding user:", error.response?.data || error.message);
        throw error;
    }
}


    return {
        user,
        signup
    };
});