# Guide d'utilisation - Clustering de Camarades

Ce guide vous aidera à utiliser l'application Clustering de Camarades, qui permet de former des groupes optimaux d'étudiants basés sur leurs affinités mutuelles.

## Table des matières

1. [Installation](#installation)
2. [Connexion et inscription](#connexion-et-inscription)
3. [Guide de l'administrateur](#guide-de-ladministrateur)
4. [Guide de l'enseignant](#guide-de-lenseignant)
5. [Guide de l'étudiant](#guide-de-létudiant)


## Installation

### Prérequis
- Node.js (v16 ou supérieur)
- Python (v3.8 ou supérieur)
- MySQL (v8.0 ou supérieur)

### Installation et démarrage

1. ****Cloner le dépôt**
   ```
   git clone https://github.com/votre-utilisateur/clusteringDeCamarades.git
   cd clusteringDeCamarades
   ```

2. **Installer et démarrer le backend**
   ```
   cd backend
   pip install -r requirements.txt
   python src/app.py
   ```

3. **Installer et démarrer le frontend**
   ```
   cd ../frontend
   npm install
   npm run dev
   ```

4. **Alternative : Utiliser le script de démarrage rapide**
   ```
   ./start.bat
   ```

5. **Accéder à l'application**
   Ouvrez votre navigateur à l'adresse : `http://localhost:5173`

## Connexion et inscription

### S'inscrire

1. Sur la page d'accueil, cliquez sur le bouton "Inscription"
2. Saisissez votre email (doit être préalablement ajouté par un administrateur)
3. Remplissez vos informations personnelles et créez un mot de passe
4. Cliquez sur "S'inscrire"

### Se connecter

1. Sur la page d'accueil, cliquez sur le bouton "Connexion"
2. Saisissez votre email et votre mot de passe
3. Cliquez sur "Se connecter"

## Guide de l'administrateur

En tant qu'administrateur, vous pouvez gérer les utilisateurs de la plateforme.

### Ajouter des utilisateurs

1. Sur la page d'accueil, cliquez sur le bouton "Administrateur"
2. Cliquez sur "Ajouter un utilisateur"
3. Saisissez l'email de l'utilisateur
4. Sélectionnez le rôle (étudiant ou enseignant)
5. Cliquez sur "Soumettre"

L'utilisateur pourra ensuite s'inscrire avec cet email.

### Gérer les utilisateurs existants

La page d'administration affiche la liste des étudiants et des enseignants. Vous pouvez:
- Voir les détails de chaque utilisateure

## Guide de l'enseignant

En tant qu'enseignant, vous pouvez créer des formulaires de vote et gérer les groupes générés.

### Créer un formulaire

1. Connectez-vous avec un compte enseignant
2. Naviguez vers "Espace professeur" sur la page d'accueil
3. Cliquez sur "Créer un formulaire"
4. Remplissez les champs requis:
   - Titre du formulaire
   - Description
   - Date de fin
   - Nombre d'étudiants par groupe
5. Optionnellement, importez une liste d'étudiants par CSV
6. Cliquez sur "Créer"

### Consulter les résultats et générer les groupes

1. Depuis le tableau de bord enseignant, cliquez sur le formulaire concerné
2. Consultez les votes et la participation des étudiants
3. Cliquez sur "Générer les groupes"
4. Visualisez les groupes proposés par l'algorithme
5. Si nécessaire, ajustez les paramètres et regénérez
6. Cliquez sur "Publier les groupes" pour les rendre visibles aux étudiants

## Guide de l'étudiant

En tant qu'étudiant, vous pouvez participer aux votes et consulter vos groupes.

### Participer à un vote

1. Connectez-vous avec un compte étudiant
2. Naviguez vers "Espace étudiant" sur la page d'accueil
3. Vous verrez la liste des formulaires disponibles
4. Cliquez sur "Participer" pour le formulaire de votre choix
5. Distribuez vos 100 points entre vos camarades:
   - Plus vous attribuez de points à une personne, plus vous augmentez vos chances d'être dans le même groupe
   - Assurez-vous que la somme des points est exactement 100
6. Cliquez sur "Soumettre mes votes"

### Consulter ses groupes

1. Depuis le tableau de bord étudiant, consultez la section "Mes groupes"
2. Vous verrez tous les groupes dans lesquels vous avez été placé
3. Pour chaque groupe, vous pouvez voir:
   - Le nom du projet/formulaire
   - Les autres membres du groupe
   - Les informations de contact



