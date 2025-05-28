<script setup>
import { ref, onMounted } from 'vue'

import { useStudentStore } from '@/store/StudentStore'
import { useTeacherStore } from '@/store/TeacherStore'
import { useAuthUserStore } from '@/store/AuthUserStore'


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
        errorMsg.value = "Invalid email, contact administrator";
        return;
    }
    try {
        await authUserStore.signup(email.value, password.value, nom.value, prenom.value);
        router.push({ name: 'home' });
    } catch (error) {
        console.error("Erreur détaillée:", error.response?.data || error);
        errorMsg.value = error.response?.data?.error || "Échec de l'inscription: veuillez contacter l'administrateur";
    }
}
</script>

<template>
  <div class="signup-container">
    <h1>Créer un compte</h1>
    <form @submit.prevent="signup" class="signup-form">
      <div class="form-group">
        <label for="email">Email :</label>
        <input id="email" v-model="email" type="email" required />
      </div>
      <div class="form-group">
        <label for="nom">Last name :</label>
        <input id="nom" v-model="nom" type="text" required />
      </div>
      <div class="form-group">
        <label for="prenom">First name :</label>
        <input id="prenom" v-model="prenom" type="text" required />
      </div>
      <div class="form-group">
        <label for="password">Password :</label>
        <input id="password" v-model="password" type="password" required />
      </div>
      <button type="submit" class="signup-button">Sign up</button>
      <p v-if="errorMsg" class="error-message">{{ errorMsg }}</p>
    </form>
    <div class="login-link">
      <p>If you already have an account, please log in</p>
      <router-link to="/login" class="login-button">Log in</router-link>
    </div>
  </div>
</template>

<style scoped>
.signup-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 20px;
}

.signup-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #333;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  transition: border 0.2s;
}

input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.signup-button {
  background-color: #3498db;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.2s;
}

.signup-button:hover {
  background-color: #2980b9;
}

.error-message {
  color: #e74c3c;
  margin-top: 10px;
  padding: 10px;
  background-color: #fadbd8;
  border-radius: 4px;
  text-align: center;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.login-button {
  display: inline-block;
  margin-top: 10px;
  color: white;
  background-color: #27ae60;
  padding: 8px 15px;
  border-radius: 4px;
  text-decoration: none;
  transition: background-color 0.2s;
}

.login-button:hover {
  background-color: #219653;
  text-decoration: none;
}

@media (max-width: 576px) {
  .signup-container {
    margin: 20px;
    padding: 15px;
  }
}
</style>