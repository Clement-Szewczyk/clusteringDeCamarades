<script setup>
import UserListItem from '@/components/admin/UserListItem.vue';
import { useStudentStore } from '@/store/StudentStore';
import { useRouter } from 'vue-router';
import { onMounted, ref } from 'vue';

const router = useRouter();
const studentStore = useStudentStore();
const loading = ref(false);
const error = ref(null);

function goToAddUser() {
    router.push({ name: 'addUser' });
}

// Charger les étudiants au montage du composant
onMounted(async () => {
    loading.value = true;
    try {
        console.log("Fetching students...");
        await studentStore.fetchStudents();
    } catch (err) {
    } finally {
        loading.value = false;
    }
});
</script>

<template>
  <h1>Admin vue</h1>
  <button @click="goToAddUser">Add Users</button>
  
  <div v-if="loading" class="loading">Chargement des données...</div>
  <div v-if="error" class="error">{{ error }}</div>
  
  <div class="lists-container">
    <ul class="half-width">
      <h1>Teachers</h1>
      <li><UserListItem email="lucien.mousin@example.com"/></li>
      <li><UserListItem email="benjamin.weinberg@example.com"/></li>
    </ul>
    
    <ul class="half-width">
      <h1>Students</h1>
      <li v-for="student in studentStore.students" :key="student.id">
        <UserListItem :email="student.student_email" />
      </li>
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
.loading, .error, .no-data {
    padding: 10px;
    margin: 10px 0;
    border-radius: 4px;
}
.loading {
    background-color: #f5f5f5;
}
.error {
    background-color: #ffeeee;
    color: #cc0000;
}
.no-data {
    background-color: #f0f0f0;
    font-style: italic;
}
</style>