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
      <ul class="navbar">
        <li>
          <a href="#" class="navbar-title" @click.prevent="goToHome">Clustering de camarades</a>
        </li>
        <li>
            <button @click="goToLogin">Login</button>
        </li>
        <li>
            <button @click="goToSignup">Signup</button>
        </li>
      </ul>
    </nav>
</template>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  list-style: none;
  padding: 0;
  gap: 1rem;
}

.navbar-title {
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
  margin-right: 2rem;
}
</style>
