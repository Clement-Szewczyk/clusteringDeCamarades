import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiCluster from '../../api/api';


export const useStudentStore = defineStore('student', () => {
    // State
    const students = ref([]);
    
    // Actions
    async function fetchStudents() {
        console.log('Fetching students...');
        try {
            const response = await apiCluster.get('students');
            console.log('Response status:', response.status);
            students.value = response.data;
        } catch (err) {
            console.error('Error fetching students:', err);
        }
    }

    async function addStudent(email) {
        try {
            const response = await apiCluster.post('students', { email: email });
            console.log('Étudiant ajouté:', response.data);
            students.value.push(response.data);
        } catch (error) {
            console.error("Erreur:", error);
        }
    }

    return {
        students,
        fetchStudents,
        addStudent
    };
});