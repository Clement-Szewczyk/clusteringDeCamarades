<script setup>
import { ref } from 'vue'

const email = ref('')
const nom = ref('')
const prenom = ref('')
const role = ref('students')
const password = ref('')

function signup() {
    console.log({
        email: email.value,
        nom: nom.value,
        prenom: prenom.value,
        role: role.value,
        password: password.value
    })
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
            <label for="role">Role :</label>
            <select id="role" v-model="role" required>
                <option value="teachers">Teacher</option>
                <option value="students">Student</option>
            </select>
        </div>
        <div>
            <label for="password">Password :</label>
            <input id="password" v-model="password" type="password" required />
        </div>
        <button type="submit">Sign up</button>
    </form>
    <p>If you already have an account, please log in</p>
    <router-link to="/login">Log in</router-link>
</template>