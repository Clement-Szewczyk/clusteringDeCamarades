<script setup>

import { useRouter } from 'vue-router';

const router = useRouter();

function goTofillingForm() {
    router.push({ name: 'fillingForm' });
} 
</script>

<template>
    <span>
        <h2>titre</h2>
        <p>description</p>
        <button @click="goTofillingForm"> Participer </button>
    </span>
</template>

<style scoped>
span{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    border-bottom: 1px solid #ccc;
}

h3 {
    margin: 0;
    flex: 1;
}
</style>