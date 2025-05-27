import pandas as pd
import numpy as np
from sklearn.cluster import SpectralClustering, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# Paramètres configurables
TAILLE_GROUPE = 5  # M personnes par groupe
NOMBRE_VOTES = None  # N votes par étudiant, sera déduit automatiquement
EXCLUSIONS = set()  # Liste des noms exclus (ex : absents)

def lire_preferences(fichier_csv):
    """Lecture et traitement des préférences depuis le CSV."""
    df = pd.read_csv(fichier_csv)
    noms = [nom for nom in df["nom"].tolist() if nom not in EXCLUSIONS]
    noms_index = {nom: i for i, nom in enumerate(noms)}
    n = len(noms)
    
    # Trouver les colonnes de votes
    colonnes_votes = [col for col in df.columns if col.startswith("choix_")]
    global NOMBRE_VOTES
    NOMBRE_VOTES = len(colonnes_votes)
    
    # Matrice d'affinité avec pondération décroissante
    affinite = np.zeros((n, n), dtype=float)
    poids_choix = list(range(NOMBRE_VOTES, 0, -1))
    
    for _, ligne in df.iterrows():
        nom = ligne["nom"]
        if nom in EXCLUSIONS or nom not in noms_index:
            continue
        i = noms_index[nom]
        for j, choix_col in enumerate(colonnes_votes):
            camarade = ligne[choix_col]
            if pd.notna(camarade) and camarade in noms_index:
                k = noms_index[camarade]
                affinite[i][k] += poids_choix[j]
    
    # Matrice symétrique avec bonus pour affinités mutuelles
    affinite_mutuelle = np.minimum(affinite, affinite.T)  # Affinités mutuelles
    affinite_unilaterale = affinite + affinite.T - 2 * affinite_mutuelle
    
    # Score final: mutuel × 1.5 + unilateral × 1.0
    affinite_finale = affinite_mutuelle * 1.5 + affinite_unilaterale * 0.5
    
    return noms, affinite_finale

def creer_features_etudiants(noms, matrice_affinite):
    """
    Transforme la matrice d'affinité en vecteurs de features pour clustering.
    Chaque étudiant devient un point dans un espace vectoriel.
    """
    n = len(noms)
    features = []
    
    for i in range(n):
        etudiant_features = []
        
        # 1. Profil de préférences émises (qui il choisit)
        preferences_emises = matrice_affinite[i, :]
        etudiant_features.extend(preferences_emises)
        
        # 2. Profil de popularité (qui le choisit)
        popularite = matrice_affinite[:, i]
        etudiant_features.extend(popularite)
        
        # 3. Métriques agrégées
        total_preferences = np.sum(preferences_emises)
        total_popularite = np.sum(popularite)
        affinites_mutuelles = np.sum(np.minimum(preferences_emises, popularite))
        
        etudiant_features.extend([
            total_preferences,      # Nombre total de "points" donnés
            total_popularite,       # Points reçus (popularité)
            affinites_mutuelles,    # Affinités réciproques
            np.max(preferences_emises),  # Affinité max émise
            np.mean(preferences_emises[preferences_emises > 0]) if np.any(preferences_emises > 0) else 0,  # Affinité moyenne
        ])
        
        features.append(etudiant_features)
    
    return np.array(features)

def clustering_spectral(noms, matrice_affinite, taille_groupe):
    """
    Clustering spectral utilisant directement la matrice d'affinité.
    Idéal pour les données de type graphe.
    """
    n = len(noms)
    k = max(1, n // taille_groupe)
    
    # Clustering spectral avec matrice d'affinité pré-calculée
    spectral = SpectralClustering(
        n_clusters=k, 
        affinity='precomputed',
        random_state=42
    )
    
    labels = spectral.fit_predict(matrice_affinite)
    
    # Organiser en clusters
    clusters = defaultdict(list)
    for i, label in enumerate(labels):
        clusters[label].append(noms[i])
    
    return dict(clusters)

def clustering_hierarchique(noms, matrice_affinite, taille_groupe):
    """
    Clustering hiérarchique agglomératif.
    Utilise la matrice d'affinité comme mesure de distance.
    """
    n = len(noms)
    k = max(1, n // taille_groupe)
    
    # Convertir affinité en distance (distance = max_affinité - affinité)
    max_affinite = np.max(matrice_affinite)
    distance_matrix = max_affinite - matrice_affinite + 0.1  # +0.1 pour éviter distance=0
    
    hierarchical = AgglomerativeClustering(
        n_clusters=k,
        metric='precomputed',
        linkage='average'
    )
    
    labels = hierarchical.fit_predict(distance_matrix)
    
    clusters = defaultdict(list)
    for i, label in enumerate(labels):
        clusters[label].append(noms[i])
    
    return dict(clusters)

def clustering_features(noms, matrice_affinite, taille_groupe):
    """
    Clustering basé sur les features des étudiants.
    Transforme les affinités en vecteurs de caractéristiques.
    """
    from sklearn.cluster import KMeans
    
    n = len(noms)
    k = max(1, n // taille_groupe)
    
    # Créer les features et normaliser
    features = creer_features_etudiants(noms, matrice_affinite)
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # K-Means sur les features normalisées
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(features_scaled)
    
    clusters = defaultdict(list)
    for i, label in enumerate(labels):
        clusters[label].append(noms[i])
    
    return dict(clusters)

def optimiser_groupes_dans_cluster(cluster_noms, matrice_affinite_globale, noms_globaux, taille_groupe):
    """
    Optimise la formation de groupes au sein d'un cluster donné.
    Utilise un algorithme glouton amélioré.
    """
    if len(cluster_noms) == 0:
        return []
    
    # Créer les indices locaux
    noms_index_global = {nom: i for i, nom in enumerate(noms_globaux)}
    indices_cluster = [noms_index_global[nom] for nom in cluster_noms]
    
    # Extraire la sous-matrice d'affinité pour ce cluster
    matrice_cluster = matrice_affinite_globale[np.ix_(indices_cluster, indices_cluster)]
    
    groupes = []
    non_assignes = set(range(len(cluster_noms)))
    
    while non_assignes:
        # Démarrer un nouveau groupe
        if len(non_assignes) >= taille_groupe:
            # Trouver la paire avec la plus forte affinité mutuelle
            meilleure_affinite = -1
            meilleur_debut = None
            
            for i in non_assignes:
                for j in non_assignes:
                    if i != j:
                        affinite_mutuelle = matrice_cluster[i, j] + matrice_cluster[j, i]
                        if affinite_mutuelle > meilleure_affinite:
                            meilleure_affinite = affinite_mutuelle
                            meilleur_debut = (i, j)
            
            if meilleur_debut:
                groupe_indices = list(meilleur_debut)
                for idx in meilleur_debut:
                    non_assignes.remove(idx)
            else:
                # Pas d'affinité mutuelle, prendre le plus populaire
                plus_populaire = max(non_assignes, key=lambda x: matrice_cluster[x, :].sum())
                groupe_indices = [plus_populaire]
                non_assignes.remove(plus_populaire)
            
            # Compléter le groupe
            while len(groupe_indices) < taille_groupe and non_assignes:
                # Trouver le candidat qui maximise l'affinité avec le groupe existant
                meilleur_candidat = max(
                    non_assignes,
                    key=lambda c: sum(matrice_cluster[c, g] + matrice_cluster[g, c] 
                                    for g in groupe_indices)
                )
                groupe_indices.append(meilleur_candidat)
                non_assignes.remove(meilleur_candidat)
            
        else:
            # Groupe final avec les restants
            groupe_indices = list(non_assignes)
            non_assignes.clear()
        
        # Convertir indices en noms
        groupe_noms = [cluster_noms[idx] for idx in groupe_indices]
        groupes.append(groupe_noms)
    
    return groupes

def calculer_score_satisfaction(groupes, matrice_affinite, noms):
    """
    Calcule le score de satisfaction global de la répartition.
    """
    noms_index = {nom: i for i, nom in enumerate(noms)}
    
    score_total = 0
    affinite_possible_totale = 0
    
    for groupe in groupes:
        if len(groupe) < 2:
            continue
        
        # Calculer l'affinité intra-groupe
        affinite_groupe = 0
        affinite_possible = 0
        
        for i in range(len(groupe)):
            for j in range(i + 1, len(groupe)):
                idx_i = noms_index[groupe[i]]
                idx_j = noms_index[groupe[j]]
                
                affinite_actuelle = matrice_affinite[idx_i, idx_j] + matrice_affinite[idx_j, idx_i]
                affinite_groupe += affinite_actuelle
                
                # Affinité possible max (si tous les choix mutuels au max)
                affinite_possible += 2 * NOMBRE_VOTES * 1.5  # Max avec bonus mutuel
        
        score_total += affinite_groupe
        affinite_possible_totale += affinite_possible
    
    satisfaction = score_total / max(affinite_possible_totale, 1)
    return satisfaction, score_total

def effectuer_clustering_complet(noms, matrice_affinite, taille_groupe=2):
    """
    Compare différentes méthodes de clustering et retourne la meilleure.
    """
    methodes = {
        'Spectral': lambda: clustering_spectral(noms, matrice_affinite, taille_groupe),
        'Hiérarchique': lambda: clustering_hierarchique(noms, matrice_affinite, taille_groupe),
        'Features K-Means': lambda: clustering_features(noms, matrice_affinite, taille_groupe)
    }
    
    resultats = {}
    
    print("🔍 Comparaison des méthodes de clustering...\n")
    
    for nom_methode, methode_func in methodes.items():
        try:
            # Effectuer le clustering
            clusters = methode_func()
            
            # Optimiser les groupes dans chaque cluster
            groupes_finaux = []
            for cluster_noms in clusters.values():
                groupes_cluster = optimiser_groupes_dans_cluster(
                    cluster_noms, matrice_affinite, noms, taille_groupe
                )
                groupes_finaux.extend(groupes_cluster)
            
            # Calculer le score
            satisfaction, score_brut = calculer_score_satisfaction(groupes_finaux, matrice_affinite, noms)
            
            resultats[nom_methode] = {
                'groupes': groupes_finaux,
                'satisfaction': satisfaction,
                'score_brut': score_brut,
                'nb_clusters': len(clusters)
            }
            
            print(f" {nom_methode:15} | Satisfaction: {satisfaction:.3f} | Score: {score_brut:.1f}")
            
        except Exception as e:
            print(f" Erreur avec {nom_methode}: {e}")
            resultats[nom_methode] = None
    
    # Trouver la meilleure méthode
    methodes_valides = {k: v for k, v in resultats.items() if v is not None}
    if methodes_valides:
        meilleure_methode = max(methodes_valides.keys(), 
                              key=lambda k: methodes_valides[k]['satisfaction'])
        return methodes_valides[meilleure_methode], meilleure_methode, resultats
    else:
        raise Exception("Aucune méthode de clustering n'a fonctionné")

def afficher_resultats_detailles(groupes, satisfaction, score_brut, methode, matrice_affinite, noms):
    """
    Affiche les résultats détaillés avec analyse des affinités.
    """
    print(f"\n RÉSULTATS - Méthode: {methode}")
    print(f"Score de satisfaction: {satisfaction:.1%}")
    print(f" Score brut: {score_brut:.1f}")
    print(f"\n GROUPES FORMÉS:\n")
    
    noms_index = {nom: i for i, nom in enumerate(noms)}
    
    for idx, membres in enumerate(groupes, 1):
        print(f" Groupe {idx}: {', '.join(membres)} ({len(membres)} personnes)")
        
        if len(membres) >= 2:
            # Analyser les affinités dans le groupe
            affinites_details = []
            for i in range(len(membres)):
                for j in range(i + 1, len(membres)):
                    nom1, nom2 = membres[i], membres[j]
                    idx1, idx2 = noms_index[nom1], noms_index[nom2]
                    
                    affinite_1_vers_2 = matrice_affinite[idx1, idx2]
                    affinite_2_vers_1 = matrice_affinite[idx2, idx1]
                    
                    if affinite_1_vers_2 > 0 or affinite_2_vers_1 > 0:
                        if affinite_1_vers_2 > 0 and affinite_2_vers_1 > 0:
                            affinites_details.append(f"   {nom1} ↔ {nom2} (mutuel: {affinite_1_vers_2:.1f} ↔ {affinite_2_vers_1:.1f})")
                        elif affinite_1_vers_2 > 0:
                            affinites_details.append(f"   {nom1} → {nom2} ({affinite_1_vers_2:.1f})")
                        else:
                            affinites_details.append(f"   {nom2} → {nom1} ({affinite_2_vers_1:.1f})")
            
            if affinites_details:
                print("\n".join(affinites_details))
            else:
                print("   Aucune affinité directe")
        print()

def afficher_groupes(groupes):
    """Version simplifiée pour compatibilité."""
    print("\n👥 Groupes formés :\n")
    for idx, membres in enumerate(groupes, 1):
        print(f"Groupe {idx}: {', '.join(membres)}")

if __name__ == "__main__":
    # Configuration
    # EXCLUSIONS.update(["Ismael", "Julia"])  # Décommenter pour exclure
    
    print("SYSTÈME DE CLUSTERING POUR FORMATION DE GROUPES")
    print("=" * 60)
    
    # Lecture des données
    noms, matrice = lire_preferences("backend/algo/preferences.csv")
    print(f" {len(noms)} étudiants chargés")
    print(f" {NOMBRE_VOTES} choix par étudiant")
    print(f"Taille de groupe cible: {TAILLE_GROUPE}")
    
    if EXCLUSIONS:
        print(f" Exclusions: {', '.join(EXCLUSIONS)}")
    
    # Effectuer le clustering
    resultat, meilleure_methode, tous_resultats = effectuer_clustering_complet(noms, matrice, TAILLE_GROUPE)
    
    # Afficher les résultats détaillés
    afficher_resultats_detailles(
        resultat['groupes'], 
        resultat['satisfaction'], 
        resultat['score_brut'],
        meilleure_methode,
        matrice,
        noms
    )