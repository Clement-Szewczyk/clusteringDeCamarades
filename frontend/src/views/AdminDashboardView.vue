<script setup>
import UserListItem from '@/components/admin/UserListItem.vue';
import { useStudentStore } from '@/store/StudentStore';
import { useTeacherStore } from '@/store/TeacherStore';

import { useRouter } from 'vue-router';
import { onMounted, ref } from 'vue';

const router = useRouter();

const studentStore = useStudentStore();
const teacherStore = useTeacherStore();

function goToAddUser() {
    router.push({ name: 'addUser' });
}

onMounted(async () => {
    try {
        console.log("Fetching students...");
        console.log("Fetching teachers...");
        await studentStore.fetchStudents();
        await teacherStore.fetchTeachers();
    } catch (err) {
      console.error("Error fetching students & teachers:", err);
    }
});
</script>

<template>
  <h1>Admin vue</h1>
  <button @click="goToAddUser">Add Users</button>
  <div class="lists-container">
    <ul class="half-width">
      <h1>Teachers</h1>
      <li v-for="teacher in teacherStore.teachers" :key="teacher.id">
        <UserListItem :email="teacher.teacher_email" />
      </li>
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