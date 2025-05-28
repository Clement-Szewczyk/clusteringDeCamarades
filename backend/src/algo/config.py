"""
Configuration module for the group clustering system.
Contains all configurable parameters and settings.
"""

# Configurable parameters
GROUP_SIZE = 3  # M people per group 
TOTAL_POINTS = 100  # Total points to distribute per student
EXCLUSIONS = set()  # List of excluded names (e.g., absent students)

# File paths
CSV_FILE_PATH = "data.csv"  # Path to the CSV file containing student data

# Algorithm parameters
MAX_ATTEMPTS = 10  # Number of different initialization strategies
MAX_LOCAL_ITERATIONS = 50  # Maximum iterations for local optimization
GLOBAL_MAX_ITERATIONS = 100  # Maximum iterations for global optimization

# Scoring weights
MUTUAL_BONUS = 1.5  # Bonus multiplier for mutual affinities
UNILATERAL_WEIGHT = 1.0  # Weight for unilateral affinities
EQUITY_WEIGHT = 100  # Weight for equity score in evaluation
SATISFACTION_WEIGHT = 10  # Weight for satisfaction score in evaluation