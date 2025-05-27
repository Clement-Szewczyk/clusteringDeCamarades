<script setup>
import { useRouter } from 'vue-router';
import NavBar from './components/NavBar.vue';
</script>

<template>
  <header>
  </header>
  <main>
    <NavBar />
    <router-view />
  </main>
</template>