<script setup>
import { useRouter } from 'vue-router';
import { defineProps, computed } from 'vue';

const props = defineProps({
  formular: {
    type: Object,
    required: true
  }
});

const router = useRouter();

const id = computed(() => props.formular.formular_id);
const title = computed(() => props.formular.title || props.formular.formular_title || "Untitled");
const description = computed(() => props.formular.description || props.formular.formular_description || "");

const endDate = computed(() => props.formular.end_date || props.formular.formular_end_date || props.formular.formular_end || "");

const nbPersonGroup = computed(() => props.formular.nb_person_group || props.formular.formular_nb_person_group || 2);

function goTofillingForm() {
  router.push({ 
    name: 'fillingForm',
    params: { id: id.value }
  });
}

function formatDate(dateString) {
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) {
      console.error('Invalid date:', dateString);
      return 'Date invalide';
    }
    return date.toLocaleDateString();
  } catch (error) {
    console.error('Error formatting date:', error);
    return 'Erreur format';
  }
}
</script>

<template>
  <span>
    <div class="formular-info">
      <h2>{{ title }}</h2>
      <p>{{ description }}</p>
      <p class="deadline">Date limite: {{ formatDate(endDate) }}</p>
      <p class="group-size">Nombre de personnes par groupe: {{ nbPersonGroup }}</p>
    </div>
    <button @click="goTofillingForm" class="participate-btn">Participer</button>
  </span>
</template>