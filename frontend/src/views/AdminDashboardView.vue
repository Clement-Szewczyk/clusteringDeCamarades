<script setup>
import UserListItem from '@/components/admin/UserListItem.vue';
import { ref } from 'vue';

const teachersFile = ref(null);
const studentsFile = ref(null);
</script>

<template>
  <h1>Admin vue</h1>
  <div class="lists-container">
    <ul class="half-width">
      <h1> Teachers </h1>
      <li><UserListItem name="Lucien" surname="Mousin"/></li>
      <li><UserListItem name="Benjamin" surname="Weinberg"/></li>
      <button> Add Teachers </button>
    </ul>
    <ul class="half-width">
      <h1> Students </h1>
      <li><UserListItem name="Carlos" surname="Okinda"/></li>
      <li><UserListItem name="Lucas" surname="Petit"/></li>
      <li><UserListItem name="Sophie" surname="Leroy"/></li>
      <button> Add Students </button>
    </ul>
  </div>
</template>

<style scoped>
.lists-container {
    display: flex;
    flex-direction: row;
    width: 100%;
}
.half-width {
    width: 50%;
    list-style: none;
    padding: 20px;
    margin: 0;
}
</style>