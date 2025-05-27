import pandas as pd
import numpy as np
from sklearn.cluster import SpectralClustering, AgglomerativeClustering, KMeans
from sklearn.preprocessing import StandardScaler
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# Configurable parameters
GROUP_SIZE = 5  # M people per group 
NUMBER_OF_VOTES = None  # N votes per student, will be automatically deduced
EXCLUSIONS = set()  # List of excluded names (e.g., absent students)

def readPreferences(csvFile):
    """Reading and processing preferences from CSV."""
    df = pd.read_csv(csvFile)
    names = [name for name in df["nom"].tolist() if name not in EXCLUSIONS]
    namesIndex = {name: i for i, name in enumerate(names)}
    n = len(names)
    
    # Find vote columns
    voteColumns = [col for col in df.columns if col.startswith("choix_")]
    global NUMBER_OF_VOTES
    NUMBER_OF_VOTES = len(voteColumns)
    
    # Affinity matrix with decreasing weighting
    affinity = np.zeros((n, n), dtype=float)
    choiceWeights = list(range(NUMBER_OF_VOTES, 0, -1))
    
    for _, row in df.iterrows():
        name = row["nom"]
        if name in EXCLUSIONS or name not in namesIndex:
            continue
        i = namesIndex[name]
        for j, choiceCol in enumerate(voteColumns):
            classmate = row[choiceCol]
            if pd.notna(classmate) and classmate in namesIndex:
                k = namesIndex[classmate]
                affinity[i][k] += choiceWeights[j]
    
    # Symmetric matrix with bonus for mutual affinities
    mutualAffinity = np.minimum(affinity, affinity.T)  # Mutual affinities
    unilateralAffinity = affinity + affinity.T - 2 * mutualAffinity
    
    # Final score: mutual × 1.5 + unilateral × 1.0
    finalAffinity = mutualAffinity * 1.5 + unilateralAffinity * 0.5
    
    return names, finalAffinity

def createStudentFeatures(names, affinityMatrix):
    """
    Transforms the affinity matrix into feature vectors for clustering.
    Each student becomes a point in a vector space.
    """
    n = len(names)
    features = []
    
    for i in range(n):
        studentFeatures = []
        
        # 1. Emitted preferences profile (who they choose)
        emittedPreferences = affinityMatrix[i, :]
        studentFeatures.extend(emittedPreferences)
        
        # 2. Popularity profile (who chooses them)
        popularity = affinityMatrix[:, i]
        studentFeatures.extend(popularity)
        
        # 3. Aggregated metrics
        totalPreferences = np.sum(emittedPreferences)
        totalPopularity = np.sum(popularity)
        mutualAffinities = np.sum(np.minimum(emittedPreferences, popularity))
        
        studentFeatures.extend([
            totalPreferences,      # Total number of "points" given
            totalPopularity,       # Points received (popularity)
            mutualAffinities,      # Reciprocal affinities
            np.max(emittedPreferences),  # Max emitted affinity
            np.mean(emittedPreferences[emittedPreferences > 0]) if np.any(emittedPreferences > 0) else 0,  # Average affinity
        ])
        
        features.append(studentFeatures)
    
    return np.array(features)

def spectralClustering(names, affinityMatrix, groupSize):
    """
    Spectral clustering using the affinity matrix directly.
    Ideal for graph-type data.
    """
    n = len(names)
    k = max(1, n // groupSize)
    
    # Spectral clustering with pre-calculated affinity matrix
    spectral = SpectralClustering(
        n_clusters=k, 
        affinity='precomputed',
        random_state=42
    )
    
    labels = spectral.fit_predict(affinityMatrix)
    
    # Organize into clusters
    clusters = defaultdict(list)
    for i, label in enumerate(labels):
        clusters[label].append(names[i])
    
    return dict(clusters)

def hierarchicalClustering(names, affinityMatrix, groupSize):
    """
    Agglomerative hierarchical clustering.
    Uses the affinity matrix as a distance measure.
    """
    n = len(names)
    k = max(1, n // groupSize)
    
    # Convert affinity to distance (distance = max_affinity - affinity)
    maxAffinity = np.max(affinityMatrix)
    distanceMatrix = maxAffinity - affinityMatrix + 0.1  # +0.1 to avoid distance=0
    
    hierarchical = AgglomerativeClustering(
        n_clusters=k,
        metric='precomputed',
        linkage='average'
    )
    
    labels = hierarchical.fit_predict(distanceMatrix)
    
    clusters = defaultdict(list)
    for i, label in enumerate(labels):
        clusters[label].append(names[i])
    
    return dict(clusters)

def featuresClustering(names, affinityMatrix, groupSize):
    """
    Clustering based on student features.
    Transforms affinities into feature vectors.
    """
    n = len(names)
    k = max(1, n // groupSize)
    
    # Create features and normalize
    features = createStudentFeatures(names, affinityMatrix)
    scaler = StandardScaler()
    scaledFeatures = scaler.fit_transform(features)
    
    # K-Means on normalized features
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(scaledFeatures)
    
    clusters = defaultdict(list)
    for i, label in enumerate(labels):
        clusters[label].append(names[i])
    
    return dict(clusters)

def forceBalancedSizeClustering(names, affinityMatrix, groupSize):
    """
    Forces the creation of balanced-size groups.
    Priority to balancing rather than cluster purity.
    """
    n = len(names)
    numberOfGroups = n // groupSize
    remainder = n % groupSize
    
    # If there's a remainder, make one more group
    if remainder > 0:
        numberOfGroups += 1
    
    # Clustering with exact number of groups
    features = createStudentFeatures(names, affinityMatrix)
    scaler = StandardScaler()
    scaledFeatures = scaler.fit_transform(features)
    
    kmeans = KMeans(n_clusters=numberOfGroups, random_state=42, n_init=10)
    labels = kmeans.fit_predict(scaledFeatures)
    
    # Organize into initial groups
    initialGroups = defaultdict(list)
    for i, label in enumerate(labels):
        initialGroups[label].append(names[i])
    
    # Balance sizes
    balancedGroups = balanceGroupSizes(
        list(initialGroups.values()), 
        groupSize, 
        affinityMatrix, 
        names
    )
    
    return {"balanced": balancedGroups}

def balanceGroupSizes(groups, targetSize, affinityMatrix, names):
    """
    Balances group sizes by optimally moving people.
    """
    namesIndex = {name: i for i, name in enumerate(names)}
    
    # Continue until groups are balanced
    maxIterations = 50
    iteration = 0
    
    while iteration < maxIterations:
        sizes = [len(g) for g in groups]
        
        # If all groups have acceptable size, stop
        if max(sizes) - min(sizes) <= 1:
            break
        
        # Find the largest and smallest groups
        maxIdx = sizes.index(max(sizes))
        minIdx = sizes.index(min(sizes))
        
        # Find the best person to move
        bestPerson = None
        bestGain = float('-inf')
        
        for person in groups[maxIdx]:
            # Calculate the gain of moving this person
            gain = calculateMovementGain(
                person, groups[maxIdx], groups[minIdx], 
                affinityMatrix, namesIndex
            )
            
            if gain > bestGain:
                bestGain = gain
                bestPerson = person
        
        # Perform the movement
        if bestPerson:
            groups[maxIdx].remove(bestPerson)
            groups[minIdx].append(bestPerson)
        
        iteration += 1
    
    return groups

def calculateMovementGain(person, sourceGroup, targetGroup, affinityMatrix, namesIndex):
    """
    Calculates the affinity gain by moving a person from one group to another.
    """
    personIdx = namesIndex[person]
    
    # Loss of affinity by leaving source group
    loss = 0
    for member in sourceGroup:
        if member != person:
            memberIdx = namesIndex[member]
            loss += affinityMatrix[personIdx, memberIdx] + affinityMatrix[memberIdx, personIdx]
    
    # Gain of affinity by joining target group
    gain = 0
    for member in targetGroup:
        memberIdx = namesIndex[member]
        gain += affinityMatrix[personIdx, memberIdx] + affinityMatrix[memberIdx, personIdx]
    
    return gain - loss

def optimizeGroupsInCluster(clusterNames, globalAffinityMatrix, globalNames, groupSize):
    """
    Optimizes group formation within a given cluster.
    Uses an improved greedy algorithm.
    """
    if len(clusterNames) == 0:
        return []
    
    # Create local indices
    globalNamesIndex = {name: i for i, name in enumerate(globalNames)}
    clusterIndices = [globalNamesIndex[name] for name in clusterNames]
    
    # Extract affinity submatrix for this cluster
    clusterMatrix = globalAffinityMatrix[np.ix_(clusterIndices, clusterIndices)]
    
    groups = []
    unassigned = set(range(len(clusterNames)))
    
    while unassigned:
        # Start a new group
        if len(unassigned) >= groupSize:
            # Find the pair with strongest mutual affinity
            bestAffinity = -1
            bestStart = None
            
            for i in unassigned:
                for j in unassigned:
                    if i != j:
                        mutualAffinity = clusterMatrix[i, j] + clusterMatrix[j, i]
                        if mutualAffinity > bestAffinity:
                            bestAffinity = mutualAffinity
                            bestStart = (i, j)
            
            if bestStart:
                groupIndices = list(bestStart)
                for idx in bestStart:
                    unassigned.remove(idx)
            else:
                # No mutual affinity, take the most popular
                mostPopular = max(unassigned, key=lambda x: clusterMatrix[x, :].sum())
                groupIndices = [mostPopular]
                unassigned.remove(mostPopular)
            
            # Complete the group
            while len(groupIndices) < groupSize and unassigned:
                # Find candidate who maximizes affinity with existing group
                bestCandidate = max(
                    unassigned,
                    key=lambda c: sum(clusterMatrix[c, g] + clusterMatrix[g, c] 
                                    for g in groupIndices)
                )
                groupIndices.append(bestCandidate)
                unassigned.remove(bestCandidate)
            
        else:
            # Final group with remaining members
            groupIndices = list(unassigned)
            unassigned.clear()
        
        # Convert indices to names
        groupNames = [clusterNames[idx] for idx in groupIndices]
        groups.append(groupNames)
    
    return groups

def redistributeUnbalancedGroups(initialGroups, affinityMatrix, names, targetSize):
    """
    Redistributes unbalanced groups after clustering.
    """
    namesIndex = {name: i for i, name in enumerate(names)}
    
    # Separate correct groups from groups that are too small
    correctGroups = []
    isolatedPeople = []
    
    for group in initialGroups:
        if len(group) >= targetSize:
            correctGroups.append(group)
        elif len(group) >= targetSize // 2:
            # Intermediate size group, keep it for now
            correctGroups.append(group)
        else:
            # Group too small, redistribute its members
            isolatedPeople.extend(group)
    
    # Redistribute isolated people
    for person in isolatedPeople:
        bestGroupIdx = -1
        bestAffinity = -1
        
        # Search for the best host group
        for idx, group in enumerate(correctGroups):
            if len(group) < targetSize:  # Group can still grow
                # Calculate affinity with this group
                totalAffinity = 0
                for member in group:
                    personIdx = namesIndex[person]
                    memberIdx = namesIndex[member]
                    totalAffinity += affinityMatrix[personIdx, memberIdx] + affinityMatrix[memberIdx, personIdx]
                
                if totalAffinity > bestAffinity:
                    bestAffinity = totalAffinity
                    bestGroupIdx = idx
        
        # Add to best group or create new group
        if bestGroupIdx >= 0:
            correctGroups[bestGroupIdx].append(person)
        else:
            # Create new group with this person
            correctGroups.append([person])
    
    return correctGroups

def calculateSatisfactionScore(groups, affinityMatrix, names):
    """
    Calculates the global satisfaction score of the distribution.
    """
    namesIndex = {name: i for i, name in enumerate(names)}
    
    totalScore = 0
    totalPossibleAffinity = 0
    
    for group in groups:
        if len(group) < 2:
            continue
        
        # Calculate intra-group affinity
        groupAffinity = 0
        possibleAffinity = 0
        
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                idxI = namesIndex[group[i]]
                idxJ = namesIndex[group[j]]
                
                currentAffinity = affinityMatrix[idxI, idxJ] + affinityMatrix[idxJ, idxI]
                groupAffinity += currentAffinity
                
                # Maximum possible affinity (if all mutual choices at max)
                possibleAffinity += 2 * NUMBER_OF_VOTES * 1.5  # Max with mutual bonus
        
        totalScore += groupAffinity
        totalPossibleAffinity += possibleAffinity
    
    satisfaction = totalScore / max(totalPossibleAffinity, 1)
    return satisfaction, totalScore

def performCompleteClustering(names, affinityMatrix, groupSize=2):
    """
    Compares different clustering methods and returns the best one.
    """
    methods = {
        'Spectral + Redistribution': lambda: clusteringWithRedistribution(names, affinityMatrix, groupSize),
        'Hierarchical + Redistribution': lambda: hierarchicalClusteringWithRedistribution(names, affinityMatrix, groupSize),
        'Balanced K-Means': lambda: forceBalancedSizeClustering(names, affinityMatrix, groupSize),
        'Classic Spectral': lambda: spectralClustering(names, affinityMatrix, groupSize),
    }
    
    results = {}
    
    print(" Comparing clustering methods (CORRECTED)...\n")
    
    for methodName, methodFunc in methods.items():
        try:
            # Perform clustering
            clusters = methodFunc()
            
            # Process according to return type
            if isinstance(clusters, dict) and "balanced" in clusters:
                # Balanced method, groups already formed
                finalGroups = clusters["balanced"]
            else:
                # Classic methods, optimize within each cluster
                finalGroups = []
                for clusterNames in clusters.values():
                    clusterGroups = optimizeGroupsInCluster(
                        clusterNames, affinityMatrix, names, groupSize
                    )
                    finalGroups.extend(clusterGroups)
                
                # Redistribute unbalanced groups
                finalGroups = redistributeUnbalancedGroups(
                    finalGroups, affinityMatrix, names, groupSize
                )
            
            # Calculate score
            satisfaction, rawScore = calculateSatisfactionScore(finalGroups, affinityMatrix, names)
            
            results[methodName] = {
                'groups': finalGroups,
                'satisfaction': satisfaction,
                'rawScore': rawScore,
                'nbClusters': len(clusters) if not isinstance(clusters, dict) or "balanced" not in clusters else len(finalGroups)
            }
            
            nbGroups = len(finalGroups)
            sizes = [len(g) for g in finalGroups]
            print(f" {methodName:25} | Satisfaction: {satisfaction:.3f} | {nbGroups} groups | Sizes: {sizes}")
            
        except Exception as e:
            print(f" Error with {methodName}: {e}")
            results[methodName] = None
    
    # Find the best method
    validMethods = {k: v for k, v in results.items() if v is not None}
    if validMethods:
        bestMethod = max(validMethods.keys(), 
                        key=lambda k: validMethods[k]['satisfaction'])
        return validMethods[bestMethod], bestMethod, results
    else:
        raise Exception("No clustering method worked")

def clusteringWithRedistribution(names, affinityMatrix, groupSize):
    """
    Spectral clustering with redistribution of unbalanced groups.
    """
    initialClusters = spectralClustering(names, affinityMatrix, groupSize)
    
    # Form groups in each cluster
    rawGroups = []
    for clusterNames in initialClusters.values():
        clusterGroups = optimizeGroupsInCluster(
            clusterNames, affinityMatrix, names, groupSize
        )
        rawGroups.extend(clusterGroups)
    
    # Redistribute
    balancedGroups = redistributeUnbalancedGroups(
        rawGroups, affinityMatrix, names, groupSize
    )
    
    return {"redistributed": balancedGroups}

def hierarchicalClusteringWithRedistribution(names, affinityMatrix, groupSize):
    """
    Hierarchical clustering with redistribution of unbalanced groups.
    """
    initialClusters = hierarchicalClustering(names, affinityMatrix, groupSize)
    
    # Form groups in each cluster
    rawGroups = []
    for clusterNames in initialClusters.values():
        clusterGroups = optimizeGroupsInCluster(
            clusterNames, affinityMatrix, names, groupSize
        )
        rawGroups.extend(clusterGroups)
    
    # Redistribute
    balancedGroups = redistributeUnbalancedGroups(
        rawGroups, affinityMatrix, names, groupSize
    )
    
    return {"redistributed": balancedGroups}

def displayDetailedResults(groups, satisfaction, rawScore, method, affinityMatrix, names):
    """
    Displays detailed results with affinity analysis.
    """
    print(f"\n FINAL RESULTS - Method: {method}")
    print(f" Satisfaction score: {satisfaction:.1%}")
    print(f" Raw score: {rawScore:.1f}")
    
    # Size statistics
    sizes = [len(g) for g in groups]
    print(f" {len(groups)} groups formed | Sizes: {sizes} | Target: {GROUP_SIZE}")
    
    print(f"\n GROUP DETAILS:\n")
    
    namesIndex = {name: i for i, name in enumerate(names)}
    
    for idx, members in enumerate(groups, 1):
        sizeEmoji = "🟢" if len(members) == GROUP_SIZE else ("🟡" if len(members) >= GROUP_SIZE//2 else "🔴")
        print(f"{sizeEmoji} Group {idx}: {', '.join(members)} ({len(members)} people)")
        
        if len(members) >= 2:
            # Analyze affinities in the group
            affinityDetails = []
            for i in range(len(members)):
                for j in range(i + 1, len(members)):
                    name1, name2 = members[i], members[j]
                    idx1, idx2 = namesIndex[name1], namesIndex[name2]
                    
                    affinity1To2 = affinityMatrix[idx1, idx2]
                    affinity2To1 = affinityMatrix[idx2, idx1]
                    
                    if affinity1To2 > 0 or affinity2To1 > 0:
                        if affinity1To2 > 0 and affinity2To1 > 0:
                            affinityDetails.append(f"    {name1} ↔ {name2} (mutual: {affinity1To2:.1f} ↔ {affinity2To1:.1f})")
                        elif affinity1To2 > 0:
                            affinityDetails.append(f"    {name1} → {name2} ({affinity1To2:.1f})")
                        else:
                            affinityDetails.append(f"    {name2} → {name1} ({affinity2To1:.1f})")
            
            if affinityDetails:
                print("\n".join(affinityDetails))
            else:
                print("    No direct affinity")
        print()

def displayGroups(groups):
    """Simplified version for compatibility."""
    print("\n Groups formed:\n")
    for idx, members in enumerate(groups, 1):
        print(f"Group {idx}: {', '.join(members)}")

if __name__ == "__main__":
    # Configuration
    # EXCLUSIONS.update(["Ismael", "Julia"])  
    
    print(" GROUP CLUSTERING SYSTEM FOR GROUP FORMATION (CORRECTED VERSION)")
    print("=" * 70)
    
    # Read data
    names, matrix = readPreferences("backend/algo/preferences.csv")
    print(f" {len(names)} students loaded")
    print(f"  {NUMBER_OF_VOTES} choices per student")
    print(f" Target group size: {GROUP_SIZE}")
    print(f" Expected number of groups: {len(names) // GROUP_SIZE} to {len(names) // GROUP_SIZE + 1}")
    
    if EXCLUSIONS:
        print(f" Exclusions: {', '.join(EXCLUSIONS)}")
    
    print("\n" + "="*70)
    
    # Perform clustering
    result, bestMethod, allResults = performCompleteClustering(names, matrix, GROUP_SIZE)
    
    print("\n" + "="*70)
    
    # Display detailed results
    displayDetailedResults(
        result['groups'], 
        result['satisfaction'], 
        result['rawScore'],
        bestMethod,
        matrix,
        names
    )
