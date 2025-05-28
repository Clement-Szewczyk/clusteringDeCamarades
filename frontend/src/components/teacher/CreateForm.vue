<script setup>
import { ref } from 'vue';
import { useFormularStore } from '@/store/FormularStore';
import { useRouter } from 'vue-router';

const router = useRouter();
const formularStore = useFormularStore();

const title = ref('');
const description = ref('');
const endDate = ref('');
const nbPersonGroup = ref(2);
const csvFile = ref(null);
const errorMessage = ref('');

async function createFormular() {
  try {
    if (!title.value || !description.value || !endDate.value || !nbPersonGroup.value) {
      errorMessage.value = 'Veuillez remplir tous les champs obligatoires';
      return;
    }
    const formData = {
      title: title.value,
      description: description.value,
      endDate: new Date(endDate.value).toISOString(),
      nbPersonGroup: parseInt(nbPersonGroup.value),
    };
    
    await formularStore.createFormular(formData);
    if (csvFile.value) {
      console.log("Un fichier CSV a été sélectionné");
    }
    router.push({ name: 'teacherDashboard' });
    
  } catch (error) {
    errorMessage.value = `Erreur lors de la création du formulaire: ${error.message}`;
  }
}

function handleFileChange(event) {
  csvFile.value = event.target.files[0];
}
</script>

<template>
  <form @submit.prevent="createFormular" class="create-form">
    <h1>Create vote</h1>
    
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
    
    <div class="form-group">
      <label for="title">Title* :</label>
      <input type="text" id="title" v-model="title" required>
    </div>
    
    <div class="form-group">
      <label for="description">Description* :</label>
      <textarea id="description" v-model="description" required></textarea>
    </div>
    
    <div class="form-group">
      <label for="endDate">Ending date* :</label>
      <input type="date" id="endDate" v-model="endDate" required>
    </div>
    
    <div class="form-group">
      <label for="nbPersonGroup">Number of persons per group* :</label>
      <input type="number" id="nbPersonGroup" v-model="nbPersonGroup" min="1" required>
    </div>
    
    <div class="form-group">
      <label for="csvFile">Upload CSV file :</label>
      <input type="file" id="csvFile" @change="handleFileChange" accept=".csv">
    </div>
    
    <button type="submit" class="submit-btn">Create</button>
  </form>
</template>
