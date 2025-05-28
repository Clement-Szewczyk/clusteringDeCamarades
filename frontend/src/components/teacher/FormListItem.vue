<script setup>
import { useRouter } from 'vue-router';
import { defineProps, computed, ref } from 'vue';
import { useClusteringStore } from '@/store/ClusteringStore';

const props = defineProps({
    formular: {
        type: Object,
        required: true
    }
});

const router = useRouter();
const clusteringStore = useClusteringStore();
const isProcessing = ref(false);
const errorMessage = ref('');

const id = computed(() => props.formular.formular_id);
const title = computed(() => props.formular.title || props.formular.formular_title || "Untitled");
const description = computed(() => props.formular.description || props.formular.formular_description || "");
const endDate = computed(() => props.formular.end_date || props.formular.formular_end_date || props.formular.formular_end || "");
const nbPersonGroup = computed(() => props.formular.nb_person_group || props.formular.formular_nb_person_group || 2);

function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString();
}

function viewFormVotes() {
  router.push({ 
    name: 'formVotes',
    params: { id: id.value }
  });
}

async function generateClusters() {
  try {
    isProcessing.value = true;
    errorMessage.value = '';
    
    await clusteringStore.generateClusters(id.value);
    
    router.push({ 
      name: 'clustering', 
      params: { id: id.value }
    });
    
  } catch (err) {
    console.error("Erreur lors de la génération des clusters:", err);
    errorMessage.value = "Échec de la génération des clusters. Veuillez réessayer.";
  } finally {
    isProcessing.value = false;
  }
}

function viewClusteringResults() {
  router.push({ 
    name: 'clustering',
    params: { id: id.value }
  });
}
</script>

<template>
  <div class="form-item">
    <div class="form-header">
      <h2>{{ title }}</h2>
      <span class="due-date">Date limite: {{ formatDate(endDate) }}</span>
    </div>
    <p class="description">{{ description }}</p>
    <p class="group-info">Taille des groupes: {{ nbPersonGroup }} personnes</p>
    
    <div class="form-actions">
      <button @click="viewFormVotes" class="view-votes-btn">Voir les votes</button>
      <button 
        @click="generateClusters" 
        class="generate-clusters-btn"
        :disabled="isProcessing"
      >
        {{ isProcessing ? 'Traitement...' : 'Générer les groupes' }}
      </button>
      <button @click="viewClusteringResults" class="view-clusters-btn">Voir les résultats</button>
    </div>
    
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<style scoped>
.form-item {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.form-item:hover {
  transform: translateY(-3px);
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.3rem;
}

.due-date {
  font-size: 0.9rem;
  color: #e74c3c;
}

.description {
  color: #555;
  margin-bottom: 10px;
}

.group-info {
  font-size: 0.9rem;
  color: #7f8c8d;
  margin-bottom: 15px;
}

.form-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

button {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.view-votes-btn {
  background-color: #3498db;
  color: white;
}

.view-votes-btn:hover:not(:disabled) {
  background-color: #2980b9;
}

.generate-clusters-btn {
  background-color: #2ecc71;
  color: white;
}

.generate-clusters-btn:hover:not(:disabled) {
  background-color: #27ae60;
}

.view-clusters-btn {
  background-color: #9b59b6;
  color: white;
}

.view-clusters-btn:hover:not(:disabled) {
  background-color: #8e44ad;
}

.error-message {
  margin-top: 10px;
  color: #e74c3c;
  background-color: #fadbd8;
  padding: 8px;
  border-radius: 4px;
}
</style>