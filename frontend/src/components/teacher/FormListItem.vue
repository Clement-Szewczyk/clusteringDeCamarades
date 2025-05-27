<script setup>
</script>

<template>
  <span>
    <h3> titre </h3>
    <p> description</p>
    <p> Created by: Teacher</p>
    <p> Date de publication </p>
    <button> Consulter </button>
    <button> Publier </button>
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