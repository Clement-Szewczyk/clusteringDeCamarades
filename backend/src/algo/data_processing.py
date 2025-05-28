"""
Module for reading and processing preference data from CSV files.
Handles weighted voting system and affinity matrix creation.
"""

import pandas as pd
import numpy as np
from config import EXCLUSIONS, TOTAL_POINTS, MUTUAL_BONUS, UNILATERAL_WEIGHT


def readPreferences(csvFile):
    """Reading and processing preferences from CSV with weighted voting system."""
    df = pd.read_csv(csvFile)
    names = [name for name in df["nom"].tolist() if name not in EXCLUSIONS]
    namesIndex = {name: i for i, name in enumerate(names)}
    n = len(names)
    
    # Find all columns that are not 'nom' (these are the weighted choices)
    choiceColumns = [col for col in df.columns if col != "nom"]
    
    # Affinity matrix
    affinity = np.zeros((n, n), dtype=float)
    
    for _, row in df.iterrows():
        name = row["nom"]
        if name in EXCLUSIONS or name not in namesIndex:
            continue
        i = namesIndex[name]
        
        # Verify that points sum to 100 (or close to it, allowing small rounding errors)
        totalPoints = 0
        validChoices = {}
        
        for choiceCol in choiceColumns:
            if pd.notna(row[choiceCol]) and row[choiceCol] > 0:
                classmate = choiceCol  # Column name is the classmate's name
                points = row[choiceCol]
                totalPoints += points
                if classmate in namesIndex:
                    validChoices[classmate] = points
        
        # Warn if points don't sum to 100 (allowing 1 point tolerance for rounding)
        if abs(totalPoints - TOTAL_POINTS) > 1:
            print(f"Warning: {name} distributed {totalPoints} points instead of {TOTAL_POINTS}")
        
        # Normalize points to ensure they sum to 100
        if totalPoints > 0:
            normalizationFactor = TOTAL_POINTS / totalPoints
            for classmate, points in validChoices.items():
                k = namesIndex[classmate]
                affinity[i][k] = points * normalizationFactor
    
    # Create final affinity matrix with mutual bonus
    mutualAffinity = np.minimum(affinity, affinity.T)  # Mutual affinities
    unilateralAffinity = affinity + affinity.T - 2 * mutualAffinity
    
    # Final score: mutual × 1.5 + unilateral × 1.0
    finalAffinity = mutualAffinity * MUTUAL_BONUS + unilateralAffinity * UNILATERAL_WEIGHT
    
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