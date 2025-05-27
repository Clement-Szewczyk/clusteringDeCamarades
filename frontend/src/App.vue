<script setup>
import NavBar from './components/NavBar.vue';
</script>

<template>
  <header>
  </header>
  <main>
    <NavBar />
    <router-view />
  </main>
  <RouterLink to="/admin">See admin page</RouterLink>
  <RouterLink to="/teacher">See teacher dashboard</RouterLink>
</template>