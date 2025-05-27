<script setup>
import { ref } from 'vue';
import { useStudentStore } from '@/store/StudentStore';
import { useRouter } from 'vue-router';
import apiCluster from '../../../api/api';

const router = useRouter();
const studentStore = useStudentStore();
const email = ref('');
const role = ref('student');

async function addUser() {
    if (role.value === 'student') {
        studentStore.addStudent(email.value)
        router.push('/admin');
    } else {
        console.log('Ajout de professeur non implémenté');
    }
}
</script>

<template>
    <div class="filling-form">
        <h1>Add user</h1>
        <p>Please add a user</p>
        <form @submit.prevent="addUser">
            <input type="email" v-model="email" placeholder="Email" required />
            <label for="role">Role :</label>
            <select id="role" v-model="role" required>
                <option value="teacher">Teacher</option>
                <option value="student">Student</option>
            </select>
            <button type="submit">Submit</button>
        </form>
    </div>
</template>

<style scoped>
.filling-form {
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
}
</style>