"""
Module containing clustering algorithms and optimization functions.
"""

import numpy as np
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.preprocessing import StandardScaler
from data_processing import createStudentFeatures
from scoring import evaluateSolution, calculateSatisfactionScore, calculateMovementGain
from config import MAX_ATTEMPTS, MAX_LOCAL_ITERATIONS


def isBeneficialMove(groups, affinityMatrix, namesIndex, personIdx, currentGroupIdx, newGroupIdx, targetSize):
    """Check if moving a person improves both equity and satisfaction"""
    person = list(namesIndex.keys())[list(namesIndex.values()).index(personIdx)]
    
    currentGroup = groups[currentGroupIdx].copy()
    newGroup = groups[newGroupIdx].copy()
    
    # Check size constraints
    currentSize = len(currentGroup)
    newSize = len(newGroup)
    
    # Don't move if it worsens equity significantly
    currentEquityLoss = abs(currentSize - targetSize) + abs(newSize - targetSize)
    newEquityLoss = abs(currentSize - 1 - targetSize) + abs(newSize + 1 - targetSize)
    
    if newEquityLoss > currentEquityLoss + 1:  # Allow small equity loss for satisfaction
        return False
    
    # Calculate satisfaction gain
    gain = calculateMovementGain(person, currentGroup, newGroup, affinityMatrix, namesIndex)
    
    return gain > 0 or newEquityLoss < currentEquityLoss


def localOptimization(groups, affinityMatrix, names, targetSize, maxIterations=MAX_LOCAL_ITERATIONS):
    """Local optimization by exchanges between groups"""
    namesIndex = {name: i for i, name in enumerate(names)}
    currentGroups = [group.copy() for group in groups]
    
    for iteration in range(maxIterations):
        improved = False
        
        for groupIdx, group in enumerate(currentGroups):
            for person in group:
                personIdx = namesIndex[person]
                
                # Try moving to other groups
                for newGroupIdx, newGroup in enumerate(currentGroups):
                    if newGroupIdx == groupIdx:
                        continue
                    
                    if isBeneficialMove(currentGroups, affinityMatrix, namesIndex, 
                                     personIdx, groupIdx, newGroupIdx, targetSize):
                        # Perform the move
                        currentGroups[groupIdx].remove(person)
                        currentGroups[newGroupIdx].append(person)
                        improved = True
                        break
                
                if improved:
                    break
            if improved:
                break
        
        if not improved:
            break
    
    return currentGroups


def forceInitialBalance(groups, targetSize):
    """Force initial balance by redistributing members"""
    # Calculate total people and ideal distribution
    totalPeople = sum(len(group) for group in groups)
    idealGroupCount = max(1, totalPeople // targetSize)
    if totalPeople % targetSize != 0:
        idealGroupCount += 1
    
    # Flatten all members
    allMembers = []
    for group in groups:
        allMembers.extend(group)
    
    # Create balanced groups
    balancedGroups = []
    membersPerGroup = totalPeople // idealGroupCount
    remainder = totalPeople % idealGroupCount
    
    start = 0
    for i in range(idealGroupCount):
        # Some groups get one extra member if there's a remainder
        groupSize = membersPerGroup + (1 if i < remainder else 0)
        end = start + groupSize
        balancedGroups.append(allMembers[start:end])
        start = end
    
    return balancedGroups


def hybridBalancedClustering(names, affinityMatrix, groupSize, maxAttempts=MAX_ATTEMPTS):
    """
    Hybrid approach combining multiple clustering methods with local optimization
    """
    n = len(names)
    targetGroupCount = max(1, n // groupSize)
    if n % groupSize != 0:
        targetGroupCount += 1
    
    bestSolution = None
    bestScore = -float('inf')
    
    # Create features for clustering
    features = createStudentFeatures(names, affinityMatrix)
    scaler = StandardScaler()
    scaledFeatures = scaler.fit_transform(features)
    
    print(f" Testing {maxAttempts} different initialization strategies...")
    
    for attempt in range(maxAttempts):
        currentGroups = None
        
        # Try different clustering approaches
        if attempt < 3:
            # K-Means with different random states
            kmeans = KMeans(n_clusters=targetGroupCount, random_state=attempt, n_init=10)
            labels = kmeans.fit_predict(scaledFeatures)
            
        elif attempt < 6:
            # Spectral clustering with different random states
            try:
                spectral = SpectralClustering(
                    n_clusters=targetGroupCount, 
                    affinity='precomputed',
                    random_state=attempt
                )
                labels = spectral.fit_predict(affinityMatrix)
            except:
                # Fallback to K-means if spectral fails
                kmeans = KMeans(n_clusters=targetGroupCount, random_state=attempt, n_init=10)
                labels = kmeans.fit_predict(scaledFeatures)
        
        else:
            # Random initialization for diversity
            labels = np.random.randint(0, targetGroupCount, size=n)
        
        # Convert labels to groups
        initialGroups = [[] for _ in range(targetGroupCount)]
        for i, label in enumerate(labels):
            initialGroups[label].append(names[i])
        
        # Remove empty groups
        initialGroups = [group for group in initialGroups if group]
        
        # Force balance if groups are too uneven
        initialGroups = forceInitialBalance(initialGroups, groupSize)
        
        # Local optimization
        optimizedGroups = localOptimization(
            initialGroups, affinityMatrix, names, groupSize, maxIterations=50
        )
        
        # Evaluate solution
        score = evaluateSolution(optimizedGroups, affinityMatrix, names, groupSize)
        satisfaction, rawScore = calculateSatisfactionScore(optimizedGroups, affinityMatrix, names)
        
        if score > bestScore:
            bestScore = score
            bestSolution = optimizedGroups.copy()
        
        # Progress indicator
        if attempt % 2 == 0:
            sizes = [len(g) for g in optimizedGroups]
            print(f"   Attempt {attempt+1:2d}: Satisfaction {satisfaction:.3f} | Sizes: {sizes}")
    
    return bestSolution