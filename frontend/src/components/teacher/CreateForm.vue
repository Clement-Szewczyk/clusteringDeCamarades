<template>
    <form>
        <h1>Create vote</h1>
        <div>
            <label for="name">Titre :</label>
            <input type="text" id="name" name="name" required>
        </div>
        <div>
            <label for="description">Description :</label>
            <textarea id="description" name="description" required></textarea>
        </div>
        <div>
            <label for="endDate">Date de fin :</label>
            <input type="date" id="endDate" name="endDate" required>
        </div>
        <div>
            <label for="votesPerPerson">Nb de votes par personne :</label>
            <input type="number" id="votesPerPerson" name="votesPerPerson" min="1" required>
        </div>
        <div>
            <label for="groupCount">Nb de groupes :</label>
            <input type="number" id="groupCount" name="groupCount" min="1" required>
        </div>
        <button type="submit">Create</button>
    </form>
</template>