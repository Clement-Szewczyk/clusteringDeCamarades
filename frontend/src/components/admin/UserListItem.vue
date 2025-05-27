<script setup>
const props = defineProps({
    name: String,
    surname: String,
});
</script>

<template>
    <span>
        <h3>{{ name }}</h3>
        <h3>{{ surname }}</h3>
        <button>Modifier</button>
        <button>Supprimer</button>
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