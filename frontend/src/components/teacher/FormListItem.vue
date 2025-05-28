<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  formular: {
    type: Object,
    required: true
  }
});

function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString();
}
</script>

<template>
  <span class="formular-item">
    <h3>{{ formular.formular_title }}</h3>
    <p class="description">{{ formular.formular_description }}</p>
    <p>Date de fin: {{ formatDate(formular.formular_end) }}</p>
    <div class="action-buttons">
      <button class="consult-btn"> Consult </button>
      <button class="publish-btn"> Publish </button>
    </div>
  </span>
</template>
