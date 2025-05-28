import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.preprocessing import StandardScaler
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# Configurable parameters
GROUP_SIZE = 3  # M people per group 
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
    
    # Final score: mutual × 1.5 + unilateral × 0.5
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

def evaluateSolution(groups, affinityMatrix, names, targetSize):
    """Evaluate a solution combining equity and satisfaction"""
    # Equity score (priority)
    groupSizes = [len(group) for group in groups]
    equityScore = -sum(abs(size - targetSize) for size in groupSizes)
    
    # Satisfaction score
    satisfaction, rawScore = calculateSatisfactionScore(groups, affinityMatrix, names)
    
    # Combined score with priority to equity
    return equityScore * 100 + satisfaction * 10

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

def localOptimization(groups, affinityMatrix, names, targetSize, maxIterations=100):
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

def hybridBalancedClustering(names, affinityMatrix, groupSize, maxAttempts=10):
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

def displayDetailedResults(groups, satisfaction, rawScore, affinityMatrix, names):
    """
    Displays detailed results with affinity analysis.
    """
    print(f"\n 🎯 FINAL RESULTS - HYBRID BALANCED CLUSTERING")
    print(f" Satisfaction score: {satisfaction:.1%}")
    print(f" Raw score: {rawScore:.1f}")
    
    # Size statistics
    sizes = [len(g) for g in groups]
    avgSize = sum(sizes) / len(sizes)
    sizeVariance = sum((size - avgSize) ** 2 for size in sizes) / len(sizes)
    
    print(f" {len(groups)} groups formed | Sizes: {sizes} | Target: {GROUP_SIZE}")
    print(f" Size balance: Avg={avgSize:.1f}, Variance={sizeVariance:.2f}")
    
    print(f"\n GROUP DETAILS:\n")
    
    namesIndex = {name: i for i, name in enumerate(names)}
    
    for idx, members in enumerate(groups, 1):
        # Size indicator
        if len(members) == GROUP_SIZE:
            sizeEmoji = "🟢"
        elif abs(len(members) - GROUP_SIZE) <= 1:
            sizeEmoji = "🟡"
        else:
            sizeEmoji = "🔴"
            
        print(f"{sizeEmoji} Group {idx}: {', '.join(members)} ({len(members)} people)")
        
        if len(members) >= 2:
            # Analyze affinities in the group
            affinityDetails = []
            totalGroupAffinity = 0
            
            for i in range(len(members)):
                for j in range(i + 1, len(members)):
                    name1, name2 = members[i], members[j]
                    idx1, idx2 = namesIndex[name1], namesIndex[name2]
                    
                    affinity1To2 = affinityMatrix[idx1, idx2]
                    affinity2To1 = affinityMatrix[idx2, idx1]
                    totalGroupAffinity += affinity1To2 + affinity2To1
                    
                    if affinity1To2 > 0 or affinity2To1 > 0:
                        if affinity1To2 > 0 and affinity2To1 > 0:
                            affinityDetails.append(f"     {name1} ↔ {name2} (mutual: {affinity1To2:.1f} ↔ {affinity2To1:.1f})")
                        elif affinity1To2 > 0:
                            affinityDetails.append(f"     {name1} → {name2} ({affinity1To2:.1f})")
                        else:
                            affinityDetails.append(f"     {name2} → {name1} ({affinity2To1:.1f})")
            
            if affinityDetails:
                print(f"    Total affinity: {totalGroupAffinity:.1f}")
                print("\n".join(affinityDetails))
            else:
                print("     No direct affinity detected")
        print()

def main():
    """Main execution function"""
    print("  HYBRID BALANCED GROUP CLUSTERING SYSTEM")
    print("=" * 70)
    
    # Configuration display
    print(f"  Configuration:")
    print(f"    Target group size: {GROUP_SIZE}")
    if EXCLUSIONS:
        print(f"    Exclusions: {', '.join(EXCLUSIONS)}")
    
    try:
        # Read data
        print(f"\n  Reading preferences from CSV...")
        names, affinityMatrix = readPreferences("backend/algo/preferences.csv")
        
        print(f"  {len(names)} students loaded")
        print(f"    {NUMBER_OF_VOTES} choices per student")
        print(f"    Expected number of groups: {len(names) // GROUP_SIZE} to {len(names) // GROUP_SIZE + 1}")
        
        print("\n" + "="*70)
        
        # Perform hybrid clustering
        print(f"  Starting hybrid balanced clustering...")
        finalGroups = hybridBalancedClustering(names, affinityMatrix, GROUP_SIZE)
        
        if finalGroups is None:
            raise Exception("Clustering failed to produce valid groups")
        
        print("\n" + "="*70)
        
        # Calculate final scores
        satisfaction, rawScore = calculateSatisfactionScore(finalGroups, affinityMatrix, names)
        
        # Display results
        displayDetailedResults(finalGroups, satisfaction, rawScore, affinityMatrix, names)
        
        # Summary statistics
        sizes = [len(g) for g in finalGroups]
        balanceScore = 1.0 - (max(sizes) - min(sizes)) / max(sizes, default=1)
        
        print("\n" + "="*70)
        print(f" SUMMARY:")
        print(f"    Satisfaction: {satisfaction:.1%}")
        print(f"    Balance Score: {balanceScore:.1%}")
        print(f"    Groups: {len(finalGroups)} | Sizes: {sizes}")
        print("=" * 70)
        
    except FileNotFoundError:
        print("  Error: Could not find 'backend/algo/preferences.csv'")
    except Exception as e:
        print(f"  Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # EXCLUSIONS.update(["StudentName1", "StudentName2"])
    
    main()