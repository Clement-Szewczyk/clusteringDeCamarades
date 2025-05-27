<script setup>

import { ref } from 'vue'

const email = ref('')
const role = ref('student')

function addUser() {
    console.log({
        email: email.value,
        role: role.value
    })
}
</script>

<template>
    <div class="filling-form">
        <h1>Add user</h1>
        <p>Please add a user</p>
        <form @submit.prevent="addUser">
            <input type="email"  v-model="email" placeholder="Email" required />
            <label for="role">Role :</label>
            <select id="role" v-model="role" required>
                <option value="teacher">Teacher</option>
                <option value="student">Student</option>
            </select>
            <button type="submit">Submit</button>
        </form>
    </div>
</template>