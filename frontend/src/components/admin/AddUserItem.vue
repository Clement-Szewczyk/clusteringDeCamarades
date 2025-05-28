<script setup>
import { ref } from 'vue';
import { useStudentStore } from '@/store/StudentStore';
import { useTeacherStore } from '@/store/TeacherStore';
import { useRouter } from 'vue-router';

const router = useRouter();
const studentStore = useStudentStore();
const teacherStore = useTeacherStore();
const email = ref('');
const role = ref('student');

async function addUser() {
    if (role.value == 'student') {
        studentStore.addStudent(email.value)
        router.push('/admin');
    } else {
        teacherStore.addTeacher(email.value)
        router.push('/admin');
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