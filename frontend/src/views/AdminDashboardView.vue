<script setup>
import UserListItem from '@/components/admin/UserListItem.vue';

import { useRouter } from 'vue-router';

const router = useRouter();

function goToAddUser() {
    router.push({ name: 'addUser' });
}
</script>

<template>
  <h1>Admin vue</h1>
  <button @click="goToAddUser" > Add Users </button>
  <div class="lists-container">
    <ul class="half-width">
      <h1> Teachers </h1>
      <li><UserListItem email="lucien.mousin@example.com"/></li>
      <li><UserListItem email="benjamin.weinberg@example.com"/></li>
        </ul>
        <ul class="half-width">
      <h1> Students </h1>
      <li><UserListItem email="carlos.okinda@example.com"/></li>
      <li><UserListItem email="lucas.petit@example.com"/></li>
      <li><UserListItem email="sophie.leroy@example.com"/></li>
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