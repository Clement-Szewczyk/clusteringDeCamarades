# main.py
"""
Main execution module for the weighted voting group clustering system.
"""

import warnings
warnings.filterwarnings('ignore')

from config import GROUP_SIZE, CSV_FILE_PATH, EXCLUSIONS
from data_processing import readPreferences
from optimization import hybridBalancedClustering
from scoring import calculateSatisfactionScore
from display import displayConfiguration, displayDetailedResults, displaySummary


def main():
    """Main execution function"""
    displayConfiguration()
    
    try:
        # Read data
        print(f"\n  Reading preferences from CSV...")
        names, affinityMatrix = readPreferences(CSV_FILE_PATH)
        
        print(f"  {len(names)} students loaded")
        print(f"    Each student distributes 100 points")
        print(f"    Expected number of groups: {len(names) // GROUP_SIZE} to {len(names) // GROUP_SIZE + 1}")
        
        print("\n" + "="*70)
        
        # Perform hybrid clustering
        print(f"  Starting weighted voting clustering...")
        finalGroups = hybridBalancedClustering(names, affinityMatrix, GROUP_SIZE)
        
        if finalGroups is None:
            raise Exception("Clustering failed to produce valid groups")
        
        print("\n" + "="*70)
        
        # Calculate final scores
        satisfaction, rawScore = calculateSatisfactionScore(finalGroups, affinityMatrix, names)
        
        # Display results
        displayDetailedResults(finalGroups, satisfaction, rawScore, affinityMatrix, names)
        
        # Display summary
        displaySummary(finalGroups, satisfaction, names)
        
    except FileNotFoundError:
        print(f"  Error: Could not find '{CSV_FILE_PATH}'")
    except Exception as e:
        print(f"  Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Uncomment to add exclusions:
    # EXCLUSIONS.update(["StudentName1", "StudentName2"])
    
    main()