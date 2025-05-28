<script setup>
import { useClusteringStore } from '@/store/ClusteringStore';
import { useFormularStore } from '@/store/FormularStore';
import { useRoute } from 'vue-router';
import { onMounted, ref, computed } from 'vue';

const route = useRoute();
const formularId = computed(() => Number(route.params.id));
const clusteringStore = useClusteringStore();
const formularStore = useFormularStore();
const formular = ref(null);

const metrics = computed(() => {
    if (!clusteringStore.clusteringResults) return null;
    return clusteringStore.clusteringResults.metrics;
});

const satisfactionPercent = computed(() => {
    if (!metrics.value || metrics.value.satisfaction === undefined) return 'N/A';
    return (metrics.value.satisfaction * 100).toFixed(1) + '%';
});

const groups = computed(() => {
    if (!clusteringStore.clusteringResults) return [];
    return clusteringStore.clusteringResults.groups || [];
});

onMounted(async () => {
    try {
        // Récupérer les détails du formulaire
        const formulars = await formularStore.fetchFormulars();
        formular.value = formulars.find(f => Number(f.formular_id) === formularId.value);
        
        if (!formular.value) {
            console.error("Formulaire non trouvé");
            return;
        }
        
        // Récupérer les résultats de clustering
        await clusteringStore.fetchClusteringResults(formularId.value);
    } catch (err) {
        console.error("Erreur lors du chargement des données:", err);
    }
});
</script>

<template>
    <div class="clustering-results">
        <h1>Résultats du clustering</h1>
        
        <div v-if="clusteringStore.loading" class="loading">
            Chargement des résultats de clustering...
        </div>
        
        <div v-else-if="clusteringStore.error" class="error-message">
            {{ clusteringStore.error }}
        </div>
        
        <div v-else-if="!clusteringStore.clusteringResults" class="no-data">
            Aucun résultat de clustering disponible pour ce formulaire.
        </div>
        
        <div v-else class="results-content">
            <div class="formular-info">
                <h2>{{ formular?.title || formular?.formular_title || 'Formulaire sans titre' }}</h2>
                <p>{{ formular?.description || formular?.formular_description || '' }}</p>
                <p>Taille des groupes : {{ formular?.nb_person_group || formular?.formular_nb_person_group || '?' }}</p>
            </div>
            
            <div class="metrics-panel">
                <h3>Métriques globales</h3>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">{{ satisfactionPercent }}</div>
                        <div class="metric-label">Satisfaction</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{{ metrics?.equity ? (metrics.equity * 100).toFixed(1) + '%' : 'N/A' }}</div>
                        <div class="metric-label">Équité</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{{ metrics?.total_score?.toFixed(1) || 'N/A' }}</div>
                        <div class="metric-label">Score total</div>
                    </div>
                </div>
            </div>
            
            <div class="groups-container">
                <h3>Groupes formés</h3>
                <div class="groups-grid">
                    <div v-for="group in groups" :key="group.id" class="group-card">
                        <h4>Groupe {{ group.id }}</h4>
                        <ul class="students-list">
                            <li v-for="student in group.students" :key="student.id" class="student-item">
                                {{ student.name }}
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.clustering-results {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

h1, h2, h3, h4 {
    color: #2c3e50;
}

h1 {
    margin-bottom: 30px;
    text-align: center;
}

.formular-info {
    margin-bottom: 30px;
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 8px;
}

.metrics-panel {
    margin-bottom: 30px;
}

.metrics-grid {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}

.metric-card {
    flex: 1;
    min-width: 200px;
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
}

.metric-value {
    font-size: 2.5rem;
    font-weight: bold;
    color: #3498db;
}

.metric-label {
    margin-top: 10px;
    font-size: 1rem;
    color: #7f8c8d;
}

.groups-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
}

.group-card {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.student-item {
    padding: 8px 0;
    border-bottom: 1px solid #f0f0f0;
}

.student-item:last-child {
    border-bottom: none;
}

.loading, .error-message, .no-data {
    padding: 30px;
    text-align: center;
    background-color: #f8f9fa;
    border-radius: 8px;
    margin: 20px 0;
}

.error-message {
    color: #e74c3c;
    background-color: #fadbd8;
}
</style>