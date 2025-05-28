# scoring.py
"""
Module for calculating satisfaction scores and evaluating group solutions.
"""

import numpy as np
from config import TOTAL_POINTS, MUTUAL_BONUS, EQUITY_WEIGHT, SATISFACTION_WEIGHT


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
                
                # Maximum possible affinity (if all points concentrated with mutual bonus)
                possibleAffinity += 2 * TOTAL_POINTS * MUTUAL_BONUS  # Max with mutual bonus
        
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
    return equityScore * EQUITY_WEIGHT + satisfaction * SATISFACTION_WEIGHT


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