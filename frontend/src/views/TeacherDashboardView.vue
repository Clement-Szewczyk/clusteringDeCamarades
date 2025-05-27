<script setup>
import FormListItem from '@/components/teacher/FormListItem.vue';
import CreateForm from '@/components/teacher/CreateForm.vue';

import { useRouter } from 'vue-router';

const router = useRouter();

function goToCreateForm() {
    router.push({ name: 'createForm' });
}

</script>
<template>
    <h1> Teacher Dashboard </h1>
    <p> This is the teacher dashboard view. </p>
    <p> Here, teachers can manage their classes and view clustering results. </p>
    <ul>
        <li> <FormListItem/> </li>
        <li> <FormListItem/> </li>
    </ul>
    <button @click="goToCreateForm"> Create a new form </button>
</template>