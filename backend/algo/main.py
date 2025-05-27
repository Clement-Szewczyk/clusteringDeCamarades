import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict

# Paramètres configurables
TAILLE_GROUPE = 3  # M personnes par groupe
NOMBRE_VOTES = None  # N votes par étudiant, sera déduit automatiquement depuis le fichier
EXCLUSIONS = set()  # Liste des noms exclus (ex : absents)

def lire_preferences(fichier_csv):
    df = pd.read_csv(fichier_csv)
    # Supposons que la colonne "nom" existe et que les colonnes votes sont toutes celles commençant par "choix_"
    noms = df["nom"].tolist()
    
    # Retirer les exclus
    noms = [nom for nom in noms if nom not in EXCLUSIONS]
    
    noms_index = {nom: i for i, nom in enumerate(noms)}
    n = len(noms)
    
    # Trouver toutes les colonnes de votes dynamiquement
    colonnes_votes = [col for col in df.columns if col.startswith("choix_")]
    global NOMBRE_VOTES
    NOMBRE_VOTES = len(colonnes_votes)
    
    affinite = np.zeros((n, n), dtype=float)
    
    # Pondération décroissante: 1er choix = N votes pts, 2e = N-1, etc.
    poids_choix = list(range(NOMBRE_VOTES, 0, -1))
    
    for _, ligne in df.iterrows():
        nom = ligne["nom"]
        if nom in EXCLUSIONS or nom not in noms_index:
            continue
        i = noms_index[nom]
        for j, choix_col in enumerate(colonnes_votes):
            camarade = ligne[choix_col]
            if camarade in noms_index:
                k = noms_index[camarade]
                affinite[i][k] += poids_choix[j]
    
    # Rendre symétrique (affinité mutuelle)
    affinite_sym = (affinite + affinite.T) / 2
    return noms, affinite_sym

def glouton_optimisation(cluster_noms, matrice_affinite, taille_groupe):
    """
    Algorithme glouton pour former des groupes dans un cluster donné,
    en maximisant la somme des affinités.
    """
    groupes = []
    non_tries = set(cluster_noms)
    noms_index = {nom: i for i, nom in enumerate(cluster_noms)}
    
    while non_tries:
        # Démarrer un groupe avec la personne ayant le plus grand nombre de liens (affinité totale)
        personne = max(non_tries, key=lambda x: matrice_affinite[noms_index[x]].sum())
        groupe_courant = [personne]
        non_tries.remove(personne)
        
        # Ajouter les meilleures affinités parmi les restants jusqu'à taille_groupe
        while len(groupe_courant) < taille_groupe and non_tries:
            # Trouver le candidat qui maximise la somme d'affinités avec le groupe
            candidats = list(non_tries)
            meilleurs_candidats = sorted(
                candidats, 
                key=lambda c: sum(matrice_affinite[noms_index[c]][noms_index[m]] for m in groupe_courant),
                reverse=True
            )
            meilleur = meilleurs_candidats[0]
            groupe_courant.append(meilleur)
            non_tries.remove(meilleur)
        
        groupes.append(groupe_courant)
    
    return groupes

def effectuer_clustering(noms, matrice_affinite, taille_groupe=3):
    n = len(noms)
    k = n // taille_groupe
    if k == 0:
        k = 1
    
    kmeans = KMeans(n_clusters=k, random_state=0, n_init="auto")
    labels = kmeans.fit_predict(matrice_affinite)
    
    clusters = defaultdict(list)
    for i, label in enumerate(labels):
        clusters[label].append(noms[i])
    
    groupes_finals = []
    for label, cluster_noms in clusters.items():
        groupes_cluster = glouton_optimisation(cluster_noms, matrice_affinite, taille_groupe)
        groupes_finals.extend(groupes_cluster)
    
    # Avertissement si groupe incomplet
    for idx, groupe in enumerate(groupes_finals):
        if len(groupe) != taille_groupe:
            print(f"Avertissement : le groupe {idx+1} a {len(groupe)} membre(s).")
    
    return groupes_finals

def afficher_groupes(groupes):
    print("\n Groupes formés :\n")
    for idx, membres in enumerate(groupes):
        print(f"Groupe {idx + 1}: {', '.join(membres)}")

if __name__ == "__main__":
    # Exemple: exclure certains absents
    ##EXCLUSIONS.update(["Ismael", "Julia"])
    
    noms, matrice = lire_preferences("backend/algo/preferences.csv")
    groupes = effectuer_clustering(noms, matrice, TAILLE_GROUPE)
    afficher_groupes(groupes)
