<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useFormularStore } from '@/store/FormularStore';
import { useStudentStore } from '@/store/StudentStore';
import { useAuthUserStore } from '@/store/AuthUserStore';
import { useVoteStore } from '@/store/VoteStore';

const route = useRoute();
const formularId = Number(route.params.id);

// Stores
const formularStore = useFormularStore();
const studentStore = useStudentStore();
const authStore = useAuthUserStore();
const voteStore = useVoteStore();

// État local
const formular = ref(null);
const loading = ref(true);
const error = ref('');
const students = ref([]);
const pointsAssignment = ref({});
const remainingPoints = ref(100);
const submitting = ref(false);

const title = computed(() => formular.value?.title || formular.value?.formular_title || "Formulaire sans titre");
const description = computed(() => formular.value?.description || formular.value?.formular_description || "");
const endDate = computed(() => formular.value?.end_date || formular.value?.formular_end_date || formular.value?.formular_end || "");
const nbPersonGroup = computed(() => formular.value?.nb_person_group || formular.value?.formular_nb_person_group || 2);
function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString();
}

const calculateRemainingPoints = () => {
  const assignedPoints = Object.values(pointsAssignment.value).reduce((sum, points) => sum + points, 0);
  remainingPoints.value = 100 - assignedPoints;
};

function updatePoints(studentId, points) {
  const numPoints = Number(points);
  if (isNaN(numPoints) || numPoints < 0) {
    pointsAssignment.value[studentId] = 0;
    calculateRemainingPoints();
    return;
  }
  
  pointsAssignment.value[studentId] = numPoints;
  calculateRemainingPoints();
  
  if (remainingPoints.value < 0) {
    console.warn(`Vous avez dépassé la limite de 100 points.`);
  }
}

async function submitForm() {
  try {
    submitting.value = true;
    const votesData = Object.entries(pointsAssignment.value)
      .filter(([, points]) => Number(points) > 0)
      .map(([studentId, points]) => ({
        student_id: Number(studentId),
        points: Number(points)
      }));
    
    if (votesData.length === 0) {
      error.value = "Vous devez attribuer des points à au moins un étudiant.";
      submitting.value = false;
      return;
    }
    
    console.log("Votes à soumettre:", votesData);
    await voteStore.submitVotes(formularId, authStore.user.id, votesData);
    
    error.value = '';
    alert("Vos votes ont été soumis avec succès!");
    
  } catch (err) {
    error.value = "Erreur lors de la soumission du formulaire: " + err.message;
    console.error("Error submitting form:", err);
  } finally {
    submitting.value = false;
  }
}

onMounted(async () => {
  try {
    loading.value = true;
    
    const formulars = await formularStore.fetchFormulars();
    formular.value = formulars.find(f => f.formular_id === formularId);
    
    if (!formular.value) {
      error.value = "Formulaire non trouvé";
      return;
    }
    
    await studentStore.fetchStudents();
    students.value = studentStore.students.filter(s => 
      s.student_email !== authStore.user.email
    );
    
    // Initialiser l'attribution de points à 0 pour chaque étudiant
    students.value.forEach(student => {
      pointsAssignment.value[student.student_id] = 0;
    });
    
  } catch (err) {
    error.value = "Erreur lors du chargement du formulaire: " + err.message;
    console.error("Error loading form data:", err);
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="filling-form">
    <!-- État de chargement -->
    <div v-if="loading" class="loading">
      Chargement du formulaire...
    </div>
    
    <!-- Message d'erreur -->
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <!-- Formulaire -->
    <div v-else>
      <!-- Détails du formulaire -->
      <div class="form-header">
        <h1>{{ title }}</h1>
        <p class="description">{{ description }}</p>
        <p class="deadline">Date limite: {{ formatDate(endDate) }}</p>
        <p class="group-info">Taille des groupes: {{ nbPersonGroup }} personnes</p>
      </div>
      
      <div class="instructions">
        <h2>Instructions</h2>
        <p>Vous disposez de 100 points à distribuer parmi vos camarades.</p>
        <p>Plus vous attribuez de points à une personne, plus vous augmentez vos chances d'être dans le même groupe.</p>
        <p class="points-remaining" :class="{ 'negative': remainingPoints < 0 }">
          Points restants: {{ remainingPoints }}
        </p>
      </div>
      
      <!-- Liste des étudiants avec attribution de points -->
      <form @submit.prevent="submitForm">
        <div class="students-list">
          <div v-for="student in students" :key="student.student_id" class="student-item">
            <div class="student-info">
              <span class="student-name">{{ student.nom }} {{ student.prenom }}</span>
              <span class="student-email">{{ student.student_email }}</span>
            </div>
            <div class="points-input">
              <input 
                type="number" 
                v-model="pointsAssignment[student.student_id]" 
                @input="updatePoints(student.student_id, pointsAssignment[student.student_id])"
                min="0" 
                max="100"
                :disabled="submitting"
              />
              <span class="points-label">points</span>
            </div>
          </div>
        </div>
        
        <div class="form-actions">
          <button type="submit" class="submit-btn" :disabled="submitting || remainingPoints < 0">
            {{ submitting ? 'Envoi en cours...' : 'Soumettre mes votes' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
