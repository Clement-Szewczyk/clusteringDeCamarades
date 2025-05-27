<script setup>
import HomeView from './views/HomeView.vue';
import { useRouter } from 'vue-router';
</script>

<template>
  <header>
  </header>
  <main>
    <nav> 
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/login">Login</router-link></li>
        <li><router-link to="/signup">Sign Up</router-link></li>
      </ul>
    </nav>
    <router-view />
  </main>
</template>