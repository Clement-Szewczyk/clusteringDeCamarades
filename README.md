# Clustering de Camarades

Ce projet a été réalisé dans le cadre de la box certificative finale de Licence 3 Sciences du Numérique.  
Il s'agit d'une **application web complète** permettant de former automatiquement des groupes de travail entre étudiants, en fonction des **affinités qu’ils expriment entre eux**.

Le but principal est de proposer une **répartition optimale et équitable** des étudiants, grâce à un algorithme de clustering personnalisé.  
L'application inclut plusieurs fonctionnalités clés :

- Authentification avec gestion des rôles (étudiant / enseignant),
- Saisie et modification des affinités,
- Lancement du clustering avec contraintes personnalisables,
- Visualisation et publication des groupes formés.

Le développement s’est appuyé sur des technologies modernes et accessibles (Vue.js, Flask, MySQL) que nous avons choisies pour leur efficacité, leur rapidité de mise en œuvre et leur adéquation avec nos compétences.

Ce document détaille les choix techniques, l’architecture générale, les algorithmes utilisés, les instructions d’installation ainsi que les tests effectués pour garantir la robustesse du projet.

## Choix technologiques

### Technologies retenues

**Frontend – Vue.js**  
Nous avons choisi **Vue.js** pour le frontend car :

- C’est un framework réactif basé sur les composants que nous avons récemment étudié en cours (Framework Web 2).
- Les trois membres du groupe le maîtrisent, ce qui a facilité le développement rapide.
- Il offre un bon équilibre entre flexibilité et structure, idéal pour gérer les formulaires d’affinité, l’authentification, et l’affichage dynamique des groupes.
- Il s’intègre facilement à une API REST, ce qui correspond parfaitement à notre backend en Flask.

**Backend – Flask**  
Nous avons hésité entre **Flask** et **FastAPI**, deux frameworks Python modernes. Notre choix s’est porté sur Flask pour les raisons suivantes :

- Bien que légèrement moins rapide que FastAPI, cette différence n’a pas d’impact significatif dans notre cas.
- Flask est très flexible, parfait pour des prototypes rapides, avec une bonne compatibilité avec les tests unitaires et les systèmes de templates.
- Clément avait déjà utilisé Flask auparavant, ce qui a permis un **gain de temps considérable** et une réduction des erreurs.
- Il permet de tout faire : authentification, gestion de session, endpoints REST, intégration de l’algorithme de clustering.

**Base de données – MySQL**

- Une base de données centralisée était nécessaire pour la **gestion des utilisateurs, des rôles, des affinités et des sessions de vote**.
- Nous avons choisi **MySQL** pour sa simplicité, sa stabilité et sa compatibilité avec SQLAlchemy sous Flask.
- Elle a permis un démarrage rapide avec un modèle de données relationnel clair.
- Elle facilite la mise en place de **droits d’accès** et le stockage structuré des affinités exprimées par les étudiants.

---

### Technologies non retenues

**Java**

- Langage puissant mais trop lourd à configurer pour un projet en temps limité.
- Nous ne nous sentions pas assez à l’aise pour développer rapidement en Java dans ces conditions.

**PHP**

- Syntaxe confuse, peu structurée sans framework.
- Moins adapté aux architectures modernes basées sur des API.
- Plus compliqué pour implémenter proprement l’algorithme de clustering.

**Symfony (framework PHP)**

- Framework complet, mais rigide et plus long à mettre en place.
- Adapté aux gros projets avec beaucoup de logique métier.
- Notre équipe est beaucoup plus à l’aise avec Vue.js et Python, donc moins de perte de temps.

**Python avec Pygame**

- Interface graphique en mode fenêtré, peu ergonomique et non adaptée aux usages web ou mobiles.
- Difficultés à gérer la communication avec des services web, ou l’intégration à une base de données.
- Pygame est plus orienté jeux que applications métiers.

---

## Interprétation du sujet

Le sujet "Clustering de Camarades" propose de développer une application capable de générer automatiquement des groupes de travail à partir des affinités exprimées entre étudiants via un formulaire.  
Notre interprétation s’est appuyée sur plusieurs éléments clés extraits du cahier des charges, que nous avons structurés comme cela :

### Objectif principal

Créer un système capable de former des groupes **équilibrés et cohérents**, en prenant en compte les **affinités entre étudiants**.  
Cela implique la mise en œuvre :

- D’un **mécanisme de collecte des affinités** sous forme de votes ou de préférences
- D’un **algorithme de clustering** optimisé pour respecter à la fois les affinités et la taille cible des groupes
- D’une **interface utilisateur fluide et intuitive** pour faciliter l’utilisation par les étudiants et les enseignants

---

### Adaptation suite au changement de consignes (Jour 2)

Le deuxième jour de l’épreuve, le sujet a été partiellement modifié.  
Initialement conçu pour former des groupes prédéfinis à partir de préférences binaires (souhaite/ne souhaite pas travailler avec quelqu’un), le sujet a évolué vers un **modèle de pondération** plus libre :

- Chaque étudiant devait **distribuer un total de 100 points** entre les autres membres de la promotion, selon ses préférences de collaboration.

Nous nous sommes rapidement adaptés :

- Le modèle d’affinité a été modifié pour **prendre en compte les pondérations personnalisées** de chaque étudiant.
- L’algorithme de clustering a été ajusté pour fonctionner avec des **valeurs d’affinité asymétriques et continues**, en recalculant la matrice d'affinité en conséquence.
- L’interface de saisie a été revue pour permettre la **répartition interactive des 100 points** dans une interface simple et contrôlée.

---

### Éléments clés du sujet

- **Affinité** : désormais représentée comme une **valeur pondérée** entre deux étudiants, exprimée librement dans la limite des 100 points. Une affinité élevée traduit un fort désir de travailler avec la personne.
- **Satisfiabilité** : score global mesurant dans quelle mesure les groupes formés respectent les pondérations exprimées. Ce score est normalisé pour permettre des comparaisons entre différentes répartitions.
- **Équité** : pénalisation intégrée pour les écarts de taille entre les groupes, afin d’assurer une répartition équilibrée.
- **Clustering dynamique** : l’enseignant peut toujours relancer le clustering avec des paramètres modifiés ou des exclusions (absences, contraintes spécifiques).

---

### Choix d'interprétation spécifiques

- Chaque étudiant **répartit 100 points** entre les autres, selon ses préférences, sans pouvoir voter pour lui-même.
- Les affinités sont **asymétriques** (A peut valoriser B plus que l’inverse).
- Les votes sont stockés sous forme de **graphe pondéré**, puis transformés en **matrice d’affinité** pour le calcul.
- L’interface vérifie en temps réel que la **somme des points est bien égale à 100**.

---

### Implications techniques

Notre interprétation du sujet, y compris l’ajustement du jour 2, nous a poussés à :

- Implémenter une **structure souple de collecte et d’analyse des votes** pondérés,
- Mettre à jour l’algorithme d’optimisation pour qu’il prenne en compte ces nouvelles pondérations,
- Garantir une **expérience utilisateur fluide** malgré l’ajout de contraintes de validation (ex. : somme des points, vote obligatoire).

Cette capacité d’adaptation nous a permis de proposer une solution fidèle aux nouvelles exigences du sujet, tout en conservant une architecture claire, modulaire et testable.

---

## Architecture

L'architecture de notre application de clustering de camarades suit une approche modulaire bien structurée. Le cœur du système repose sur un **backend** qui centralise la logique métier, incluant l'API, les tests et les algorithmes de clustering. Ce backend s'appuie sur une **database** pour stocker et gérer les données de l'application, tandis qu'un dossier **docs** contient toute la documentation technique et les guides utilisateur.

Le **frontend** constitue l'interface utilisateur avec ses assets, composants, vues, système de routage, store et API. L'ensemble est orchestré par un fichier **README.md** qui fournit la documentation générale du projet, et un script **start.bat** qui permet de lancer facilement l'application.

Cette séparation claire entre les couches (présentation, logique métier, données et documentation) garantit une maintenabilité optimale et facilite le développement collaboratif, tout en permettant une évolutivité future du système de formation de groupes d'étudiants.

## Fonctionnement de l’algorithme

Notre algorithme repose sur un système de **vote pondéré** dans lequel chaque étudiant dispose de **100 points** à répartir entre ses camarades, dans le but de **former des groupes optimaux**. L’objectif principal est de **maximiser la satisfaction globale**, tout en respectant une **équité des tailles de groupes**.

---

### 1. Système de points et affinités

#### Distribution des points par étudiant

- Chaque étudiant dispose de **100 points à répartir librement** entre ses camarades.
- Exemple : Alice peut attribuer 50 points à Bob, 30 à Charlie et 20 à Eve.
- Si la somme n’est pas exactement égale à 100, l'algorithme applique une **normalisation proportionnelle** automatique.

#### Calcul de l’affinité entre deux étudiants

Pour chaque paire d’étudiants A et B :

- `Affinity_mutual = min(points_A→B, points_B→A)`
- `Affinity_unilateral = (points_A→B + points_B→A) - 2 × Affinity_mutual`
- **Score_final = Affinity_mutual × 1.5 + Affinity_unilateral × 1.0**

##### Exemples :

| A → B | B → A | Mutual | Unilateral | Score final       |
| ----- | ----- | ------ | ---------- | ----------------- |
| 40    | 30    | 30     | 20         | 30×1.5 + 20 = 65  |
| 25    | 25    | 25     | 0          | 25×1.5 + 0 = 37.5 |
| 50    | 0     | 0      | 50         | 0 + 50 = 50       |
| 0     | 0     | 0      | 0          | 0                 |

---

### 2. Calcul du score d’un groupe

Pour un groupe de `n` étudiants, on calcule la **somme des affinités finales** de toutes les paires :

```
Score_groupe = ∑(i=1 to n-1) ∑(j=i+1 to n) Score_final(i,j)
```

## Score maximum théorique

```
Max = C(n,2) × 2 × 100 × 1.5 = (n×(n−1)/2) × 300
```

| Taille | Max théorique |
| ------ | ------------- |
| 3      | 900           |
| 4      | 1800          |
| 5      | 3000          |

## 3. Satisfaction globale

```
Satisfaction = Score_total / Score_max_possible
```

**Exemple :**

- Groupe 1 : 1200 / 3000
- Groupe 2 : 800 / 3000
- Satisfaction globale = (1200 + 800) / (3000 + 3000) = 33.3%

## 4. Bonus d'affinité mutuelle

Les votes réciproques sont valorisés :

- Bonus de ×1.5 appliqué aux affinités mutuelles
- Encourage la coopération bilatérale

## 5. Optimisation locale

L'algorithme tente d'échanger des membres entre groupes :

```python
if gain_affinity > 0 or gain_equity > seuil:
    accepter le déplacement
```

**Critères d'arrêt :**

- Aucun échange bénéfique trouvé
- 50 itérations atteintes
- Convergence du score

## 6. Score global

```
Score_global = Équité × 100 + Satisfaction × 10
```

L'équité est prioritaire :

- Un groupe mal équilibré coûte -100 points
- Il faut +10% de satisfaction pour compenser

## 7. Étapes de l'algorithme

**Prétraitement :**

- Lecture des votes
- Normalisation à 100 points
- Construction de la matrice d'affinité

**Clustering initial :**

- 10 essais : 3 KMeans, 3 Spectral, 4 aléatoires
- Équilibrage des groupes

**Optimisation locale :**

- Échanges entre groupes si gain détecté

**Sélection finale :**

- Meilleur score global retenu

## 8. Exemple complet

**6 étudiants, 2 groupes de 3 :**

**Votes :**

- Alice → Bob: 60, Charlie: 40
- Bob → Alice: 50, Diana: 50
- Charlie → Alice: 30, Eve: 70
- Diana → Bob: 80, Frank: 20
- Eve → Charlie: 40, Frank: 60
- Frank → Diana: 45, Eve: 55

**Groupes finaux :**

- Groupe 1 : Alice, Bob, Diana → Score : 180
- Groupe 2 : Charlie, Eve, Frank → Score : 168.75

**Satisfaction :** 348.75 / 1800 = 19.4%

Ce fonctionnement garantit une répartition cohérente, équitable et personnalisée des étudiants, respectant à la fois leurs préférences et les contraintes pédagogiques.
