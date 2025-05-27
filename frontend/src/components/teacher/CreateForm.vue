<template>
    <form>
        <h1>Create vote</h1>
        <div>
            <label for="name">Title :</label>
            <input type="text" id="name" name="name" required>
        </div>
        <div>
            <label for="description">Description :</label>
            <textarea id="description" name="description" required></textarea>
        </div>
        <div>
            <label for="endDate">Ending date :</label>
            <input type="date" id="endDate" name="endDate" required>
        </div>
        <div>
            <label for="votesPerPerson">Number of vote (per person) :</label>
            <input type="number" id="votesPerPerson" name="votesPerPerson" min="1" required>
        </div>
        <div>
            <label for="groupCount">Number of groups :</label>
            <input type="number" id="groupCount" name="groupCount" min="1" required>
        </div>
        <div>
            <label for="csvFile">Upload CSV file :</label>
            <input type="file" id="csvFile" name="csvFile" accept=".csv">
        </div>
        <button type="submit">Create</button>
    </form>
</template>