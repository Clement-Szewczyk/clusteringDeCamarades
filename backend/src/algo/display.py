"""
Module for displaying results and generating detailed output.
"""

from config import GROUP_SIZE


def displayDetailedResults(groups, satisfaction, rawScore, affinityMatrix, names):
    """
    Displays detailed results with affinity analysis.
    """
    print(f"\n  FINAL RESULTS - WEIGHTED VOTING CLUSTERING")
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


def displayConfiguration():
    """Display current configuration settings"""
    from config import GROUP_SIZE, TOTAL_POINTS, EXCLUSIONS
    
    print("  WEIGHTED VOTING GROUP CLUSTERING SYSTEM")
    print("=" * 70)
    
    print(f"  Configuration:")
    print(f"    Target group size: {GROUP_SIZE}")
    print(f"    Points per student: {TOTAL_POINTS}")
    if EXCLUSIONS:
        print(f"    Exclusions: {', '.join(EXCLUSIONS)}")


def displaySummary(finalGroups, satisfaction, names):
    """Display final summary statistics"""
    sizes = [len(g) for g in finalGroups]
    balanceScore = 1.0 - (max(sizes) - min(sizes)) / max(sizes, default=1)
    
    print("\n" + "="*70)
    print(f" SUMMARY:")
    print(f"    Satisfaction: {satisfaction:.1%}")
    print(f"    Balance Score: {balanceScore:.1%}")
    print(f"    Groups: {len(finalGroups)} | Sizes: {sizes}")
    print("=" * 70)