<script setup>
</script>

<template>
  <span>
    <h3> Title </h3>
    <p> Description </p>
    <p> Created by: Teacher</p>
    <p> Publication date </p>
    <button> Consult </button>
    <button> Publish </button>
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