"""
Module for calculating satisfaction scores and evaluating group solutions.

This module provides functions to measure the quality of clustering solutions
by calculating satisfaction scores based on student preferences (affinity matrix),
evaluating overall solutions, and calculating potential gains from group changes.
"""

import numpy as np
from config import TOTAL_POINTS, MUTUAL_BONUS, EQUITY_WEIGHT, SATISFACTION_WEIGHT


def calculateSatisfactionScore(groups, affinityMatrix, names):
    """
    Calculates the global satisfaction score of the distribution.
    
    Computes how satisfied students would be with their assigned groups
    by measuring affinity within each group compared to the maximum possible.
    
    Args:
        groups (list): List of groups, each containing list of student names
        affinityMatrix (numpy.ndarray): Matrix containing affinity scores between students
        names (list): List of all student names
        
    Returns:
        tuple: (satisfaction_ratio, raw_satisfaction_score)
            - satisfaction_ratio: Score from 0-1 indicating overall satisfaction
            - raw_satisfaction_score: Total affinity points in the solution
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
    """
    Evaluate a solution combining equity and satisfaction.
    
    Creates a composite score balancing group size equity and student satisfaction.
    
    Args:
        groups (list): List of groups, each containing list of student names
        affinityMatrix (numpy.ndarray): Matrix containing affinity scores between students
        names (list): List of all student names
        targetSize (int): Ideal size for each group
        
    Returns:
        float: Composite score where higher values indicate better solutions
    """
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
    
    Measures the net change in affinity when a student moves between groups.
    
    Args:
        person (str): Name of the student being moved
        sourceGroup (list): List of student names in the source group
        targetGroup (list): List of student names in the target group
        affinityMatrix (numpy.ndarray): Matrix containing affinity scores between students
        namesIndex (dict): Dictionary mapping student names to matrix indices
        
    Returns:
        float: Net affinity gain (positive) or loss (negative) from the move
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