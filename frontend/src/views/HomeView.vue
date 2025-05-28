<script setup></script>
<template>
    <div class="home-container">
        <h1>Clustering de Camarades</h1>
        <p class="welcome-message">Bienvenue dans l'application de clustering de camarades des Yétis Cactus Épiques</p>
        
        <div class="dashboard-links">
            <RouterLink to="/admin" class="dashboard-link admin">Administration</RouterLink>
            <RouterLink to="/teacher" class="dashboard-link teacher">Espace professeur</RouterLink>
            <RouterLink to="/student" class="dashboard-link student">Espace étudiant</RouterLink>
        </div>
        
        <div class="clustering-section">
            <h2>Résultats de clustering récents</h2>
            <p>Accédez directement aux résultats de clustering des formulaires récents :</p>
            
            <!-- Liste simplifiée des formulaires avec des résultats de clustering -->
            <div class="recent-clustering-list">
                <RouterLink to="/clustering/1" class="clustering-link">
                    Résultats du formulaire 1
                </RouterLink>
                <RouterLink to="/clustering/2" class="clustering-link">
                    Résultats du formulaire 2
                </RouterLink>
                <!-- Dans une version plus avancée, ces liens seraient générés dynamiquement -->
            </div>
        </div>
    </div>
</template>

<style scoped>
.home-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 30px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 20px;
}

h2 {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-top: 40px;
  margin-bottom: 15px;
}

.welcome-message {
  font-size: 1.2rem;
  color: #555;
  margin-bottom: 40px;
}

.dashboard-links {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 30px;
}

.dashboard-link {
  display: block;
  padding: 15px;
  border-radius: 6px;
  color: white;
  font-weight: bold;
  text-decoration: none;
  font-size: 1.1rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.dashboard-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.admin {
  background-color: #e74c3c;
}

.teacher {
  background-color: #3498db;
}

.student {
  background-color: #27ae60;
}

.clustering-section {
  margin-top: 50px;
  padding-top: 30px;
  border-top: 1px solid #eee;
}

.recent-clustering-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

.clustering-link {
  display: block;
  padding: 12px;
  background-color: #9b59b6;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  transition: background-color 0.2s, transform 0.2s;
}

.clustering-link:hover {
  background-color: #8e44ad;
  transform: translateY(-2px);
}

@media (min-width: 768px) {
  .dashboard-links {
    flex-direction: row;
    justify-content: center;
    gap: 20px;
  }
  
  .dashboard-link {
    flex: 1;
    max-width: 200px;
  }
}
</style>