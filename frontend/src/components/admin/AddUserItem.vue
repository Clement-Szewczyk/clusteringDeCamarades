<script setup>

import { ref } from 'vue'

const email = ref('')
const role = ref('students')

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
    <div class="filling-form">
        <h1>Add user</h1>
        <p>Please add a user</p>
        <form>
            <input type="email"  v-model="email" placeholder="Email" required />
            <label for="role">Role :</label>
            <select id="role" v-model="role" required>
                <option value="teachers">Teacher</option>
                <option value="students">Student</option>
            </select>
            <button type="submit">Submit</button>
        </form>
    </div>
</template>