import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiCluster from '../../api/api';

export const useAuthUserStore = defineStore('user', () => {
    // State
    const user = ref(null);
    
    // Initialiser l'utilisateur depuis le localStorage au chargement
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
        try {
            user.value = JSON.parse(storedUser);
        } catch (e) {
            localStorage.removeItem('user');
        }
    }
    
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
            // Sauvegarder l'utilisateur dans localStorage
            localStorage.setItem('user', JSON.stringify(response.data));
            // Sauvegarder le token s'il existe
            if (response.data.token) {
                localStorage.setItem('authToken', response.data.token);
            }
            return response.data;
        } catch (error) {
            console.error("Error adding user:", error.response?.data || error.message);
            throw error;
        }
    }

    // AuthUserStore.js
    async function login(email, password) {
    try {
        console.log("Trying to log in user", { email, password });
        const response = await apiCluster.post('auth/login', { 
            email: email,
            password: password
        });
        console.log('User logged in:', response.data);
        
        // Stocker le token dans localStorage pour les requêtes futures
        if (response.data.token) {
            localStorage.setItem('authToken', response.data.token);
        }
        user.value = response.data.user || response.data; 
        localStorage.setItem('user', JSON.stringify(user.value));
        console.log('User value after login:', user.value);
        
        return response.data;
    } catch (error) {
        console.error("Error logging in user:", error.response?.data || error.message);
        throw error;
    }
}
    
    // Fonction pour vérifier si l'utilisateur est connecté
    function isLoggedIn() {
        return !!user.value;

    }
    
    // Fonction pour déconnecter l'utilisateur
    function logout() {
        user.value = null;
        localStorage.removeItem('user');
        localStorage.removeItem('authToken');
    }

    return {
        user,
        signup,
        login,
        isLoggedIn,
        logout
    };
});