import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiCluster from '../../api/api';


export const useTeacherStore = defineStore('teacher', () => {
    // State
    const teachers = ref([]);
    
    // Actions
    async function fetchTeachers() {
        console.log('Fetching teachers...');
        try {
            const response = await apiCluster.get('teachers');
            console.log('Response status:', response.status);
            teachers.value = response.data;
        } catch (err) {
            console.error('Error fetching teachers:', err);
        }
    }

    async function addTeacher(email) {
        try {
            const response = await apiCluster.post('teachers', { email: email });
            console.log('Teacher ajouté:', response.data);
            teachers.value.push(response.data);
        } catch (error) {
            console.error("Erreur:", error);
        }
    }

    return {
        teachers,
        fetchTeachers,
        addTeacher
    };
});