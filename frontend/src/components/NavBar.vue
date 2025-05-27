<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

function goToLogin() {
    router.push({ name: 'login' });
}

function goToSignup() {
    router.push({ name: 'signup' });
}

function goToHome() {
    router.push({ name: 'home' });
}

</script>

<template>
    <nav> 
      <ul>
        <h1> Clustering de camarades </h1>
        <li>
            <button @click="goToHome">Home</button>
        </li>
        <li>
            <button @click="goToLogin">Go to Login</button>
        </li>
        <li>
            <button @click="goToSignup">Go to Signup</button>
        </li>
      </ul>
    </nav>
</template>