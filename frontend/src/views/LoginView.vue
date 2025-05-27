<script setup>
import { ref } from 'vue'

const email = ref('')
const password = ref('')

function handleLogin() {
    console.log('Email:', email.value)
    console.log('Password:', password.value)
}
</script>

<template>
    <p> This is the login view. </p>
    <p> You can log in here. </p>
    <form @submit.prevent="handleLogin">
        <div>
            <label for="email">Email :</label>
            <input id="email" v-model="email" type="email" required />
        </div>
        <div>
            <label for="password">Password :</label>
            <input id="password" v-model="password" type="password" required />
        </div>
        <button type="submit">Log in</button>
    </form>
    <p> If you don't have an account, please sign up. </p>
    <router-link to="/signup">Sign up</router-link>
</template>