<script setup>
import FormListItem from '@/components/teacher/FormListItem.vue';
import { useFormularStore } from '@/store/FormularStore';
import { useAuthUserStore } from '@/store/AuthUserStore';
import VoteList from '@/components/student/VoteList.vue';
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';

const router = useRouter();
const formularStore = useFormularStore();
const authStore = useAuthUserStore();

function goToCreateForm() {
  router.push({ name: 'createForm' });
}

onMounted(async () => {
  try {
    console.log("Fetching teacher formulars...");
    await formularStore.fetchCurrentTeacherFormulars();
  } catch (err) {
    console.error("Error fetching formulars:", err);
  }
});
</script>

<template>
  <div class="teacher-dashboard">
    <h1>Mes formulaires</h1>
    <button @click="goToCreateForm" class="create-btn">Créer un formulaire</button>
    
    <div class="loading-indicator" v-if="formularStore.loading">
      Chargement des formulaires...
    </div>
    
    <div class="no-forms" v-else-if="formularStore.formulars.length === 0">
      Vous n'avez pas encore créé de formulaire.
    </div>
    
    <ul class="formulars-list" v-else>
      <li v-for="formular in formularStore.formulars" :key="formular.formular_id">
        <FormListItem :formular="formular" />
      </li>
    </ul>
  </div>
<VoteList :formularId="selectedFormularId" />
</template>

<style scoped>
</style>