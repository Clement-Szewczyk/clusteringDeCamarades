<script setup>
const props = defineProps({
    email: String,
});
</script>

<template>
    <span>
        <h3>{{ email }}</h3>
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