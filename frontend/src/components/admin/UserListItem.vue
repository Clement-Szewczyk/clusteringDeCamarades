<script></script>

<template>
    <span>
        <h3> Nom </h3>
        <h3> Prénom </h3>
        <h3> Role </h3>
        <button> Modifier </button>
        <button> Supprimer </button>
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