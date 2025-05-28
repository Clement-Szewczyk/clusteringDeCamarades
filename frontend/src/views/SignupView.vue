<script setup>
import { ref, onMounted } from 'vue'

import { useStudentStore } from '@/store/StudentStore'
import { useTeacherStore } from '@/store/TeacherStore'
import { useAuthUserStore } from '@/store/AuthUserStore'
import { all } from 'axios'

const studentStore = useStudentStore()
const teacherStore = useTeacherStore()
const authUserStore = useAuthUserStore()

const email = ref('')
const nom = ref('')
const prenom = ref('')
const password = ref('')
const errorMsg = ref('')

const allowedEmails = ref([])

onMounted(async () => {
    await studentStore.fetchStudents()
    await teacherStore.fetchTeachers()
    const studentEmails = studentStore.students.map(s => s.student_email)
    const teacherEmails = teacherStore.teachers.map(t => t.teacher_email)
    allowedEmails.value = [...studentEmails, ...teacherEmails]
    console.log(allowedEmails.value)
})


async function signup() {
    errorMsg.value = '';
    if (!allowedEmails.value.includes(email.value)) {
        errorMsg.value = "Email not authorized for signup.";
        return;
    }
    try {
        await authUserStore.signup(email.value, password.value, nom.value, prenom.value);
    } catch (error) {
        errorMsg.value = error.response?.data?.error || "Failed to register. Please try again.";
    }
}
</script>

<template>
    <form @submit.prevent="signup">
        <div>
            <label for="email">Email :</label>
            <input id="email" v-model="email" type="email" required />
        </div>
        <div>
            <label for="nom">Last name :</label>
            <input id="nom" v-model="nom" type="text" required />
        </div>
        <div>
            <label for="prenom">First name :</label>
            <input id="prenom" v-model="prenom" type="text" required />
        </div>
        <div>
            <label for="password">Password :</label>
            <input id="password" v-model="password" type="password" required />
        </div>
        <button type="submit">Sign up</button>
        <p v-if="errorMsg" style="color:red">{{ errorMsg }}</p>
    </form>
    <p>If you already have an account, please log in</p>
    <router-link to="/login">Log in</router-link>
</template>