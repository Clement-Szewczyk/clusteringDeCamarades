<script setup>
import FormListItem from '@/components/student/FormListItem.vue';
import { useFormularStore } from '@/store/FormularStore';
import VoteList from '@/components/student/VoteList.vue';
import { onMounted } from 'vue';

const formularStore = useFormularStore();

onMounted(async () => {
  try {
    console.log("Fetching available formulars for students...");
    await formularStore.fetchFormulars();
    console.log("Formulars data:", formularStore.formulars); // Pour déboguer
  } catch (err) {
    console.error("Error fetching formulars:", err);
  }
});
</script>

<template>
  <h1>Students Dashboard</h1>
  <p>Here, students can fill their clustering form</p>
  
  <div v-if="formularStore.loading" class="loading">
    Chargement des formulaires...
  </div>
  
  <div v-else-if="formularStore.formulars.length === 0" class="no-forms">
    Aucun formulaire disponible actuellement.
  </div>
  
  <ul v-else class="formulars-list">
    <li v-for="formular in formularStore.formulars" :key="formular.formular_id">
      <FormListItem :formular="formular" />
    </li>
  </ul>
<VoteList :formularId="selectedFormularId" />
</template>

<style scoped>
h1 {
  color: #2c3e50;
  margin-bottom: 10px;
}

p {
  color: #7f8c8d;
  margin-bottom: 30px;
}

.loading, .no-forms {
  padding: 15px;
  margin: 20px 0;
  border-radius: 4px;
  text-align: center;
}

.loading {
  background-color: #f5f5f5;
  color: #666;
}

.no-forms {
  background-color: #f9f9f9;
  color: #666;
  font-style: italic;
}

.formulars-list {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

@media (max-width: 768px) {
  .formulars-list {
    grid-template-columns: 1fr;
  }
}
</style>