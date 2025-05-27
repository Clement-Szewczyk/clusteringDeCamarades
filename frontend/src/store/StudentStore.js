import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useStudentStore = defineStore('student', () => {
    // State
    const students = ref([]);
    
    // Actions
    async function fetchStudents() {
        console.log('Fetching students...');
        try {
            const response = await fetch('http://localhost:5000/students');
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            students.value = await response.json();
            console.log('Fetched students:', students.value);
        } catch (err) {
            console.error('Error fetching students:', err);
            error.value = err.message;
        } finally {
            loading.value = false;
        }
    }

    async function addStudent(email) {
        loading.value = true;
        error.value = null;
        try {
            const response = await fetch('http://localhost:5000/students', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email }),
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
            }
            
            const newStudent = await response.json();
            students.value.push(newStudent);
            return newStudent;
        } catch (err) {
            console.error('Error adding student:', err);
            error.value = err.message;
            throw err;
        } finally {
            loading.value = false;
        }
    }

    return {
        students,
        fetchStudents,
        addStudent
    };
});