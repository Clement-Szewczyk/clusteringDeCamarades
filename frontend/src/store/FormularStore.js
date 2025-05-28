import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiCluster from '../../api/api';
import { useAuthUserStore } from './AuthUserStore';

export const useFormularStore = defineStore('formular', () => {
    // State
    const formulars = ref([]);
    const loading = ref(false);
    
    // Actions
    async function fetchFormulars() {
        console.log('Fetching formulars...');
        try {
            loading.value = true;
            const response = await apiCluster.get('formulars');
            console.log('Response status:', response.status);
            formulars.value = response.data;
            return formulars.value;
        } catch (err) {
            console.error('Error fetching formulars:', err);
        } finally {
            loading.value = false;
        }
    }
    
    async function fetchTeacherFormulars(teacherId) {
        console.log(`Fetching formulars for teacher ${teacherId}...`);
        try {
            loading.value = true;
            const response = await apiCluster.get(`teachers/${teacherId}/formulars`);
            console.log('Response status:', response.status);
            formulars.value = response.data;
            return formulars.value;
        } catch (err) {
            console.error('Error fetching teacher formulars:', err);
        } finally {
            loading.value = false;
        }
    }
    
    async function fetchCurrentTeacherFormulars() {
        const authStore = useAuthUserStore();
        if (!authStore.user || !authStore.user.id) {
            console.error('User not authenticated or not a teacher');
            return [];
        }
        return await fetchTeacherFormulars(authStore.user.id);
    }

    async function createFormular(formData) {
        try {
            const authStore = useAuthUserStore();
            if (!authStore.user) {
                throw new Error('User not authenticated');
            }
            let formattedEndDate;
            if (formData.endDate instanceof Date) {
                formattedEndDate = formData.endDate.toISOString().split('.')[0];
            } else {
                formattedEndDate = formData.endDate.split('.')[0];
            }
            
            console.log('Creating formular with data:', {
                title: formData.title,
                description: formData.description,
                creator_id: authStore.user.id || null,
                end_date: formattedEndDate,
                nb_person_group: Number(formData.nbPersonGroup)
            });
            
            const response = await apiCluster.post('formulars', {
                title: formData.title,
                description: formData.description,
                creator_id: authStore.user.id || null,
                end_date: formattedEndDate,
                nb_person_group: Number(formData.nbPersonGroup)
            });
            
            console.log('Formular created:', response.data);
            formulars.value.push(response.data);
            return response.data;
        } catch (error) {
            console.error("Error creating formular:", error);
            if (error.response) {
                console.error("Server response:", error.response.status, error.response.data);
            }
            throw error;
        }
    }

    return {
        formulars,
        loading,
        fetchFormulars,
        fetchTeacherFormulars,
        fetchCurrentTeacherFormulars,
        createFormular,
    };
});