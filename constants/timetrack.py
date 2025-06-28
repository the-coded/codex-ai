"""
Time tracking constants for Git commit analysis.

This module contains all constants used for calculating development time
based on Git commit history, file types, complexity analysis, and commit patterns.

IMPORTANT: These values are based on empirical analysis of development patterns
and should be calibrated based on your team's actual performance data.

## 📊 METHODOLOGY EXPLANATION

### Base Time Calculation Logic:
The time estimation is split into two phases:
1. **Planning Time**: Time spent thinking, designing, and understanding the problem
2. **Implementation Time**: Time spent actually writing/modifying code

### File Type Categories:
Different file types require different cognitive loads:
- **LOGIC files** (js/ts): High cognitive load, complex logic, more planning needed
- **STYLE files** (css/scss): Medium cognitive load, visual feedback, iterative process  
- **CONFIG files** (json/yml): Low cognitive load, mostly copy/paste or simple edits
- **DOCS files** (md/txt): Low cognitive load, mostly writing and formatting

### Time Per Line Rationale:
Based on industry studies and empirical observation:
- Average developer types 40-80 lines of code per hour when focused
- This includes thinking, testing, debugging, not just typing
- Different file types have different "thinking to typing" ratios

### Complexity Multipliers:
Based on cognitive load theory:
- Simple changes: Pattern matching, minimal context switching
- Complex changes: Deep understanding, multiple system interactions
- Structural vs Algorithmic: Different types of cognitive load
"""

from typing import Dict, List, Any

# ===== ESSENTIAL FILE CATEGORIES =====
#
# 📊 EXPLANATION:
# Only the 4 categories actually used by the timetracker system.
# Based on: old/pkg/timetracker/analyze-git-changes.js

FILE_CATEGORIES = {
    "LOGIC": {
        "extensions": ["js", "ts", "jsx", "tsx"],
        "description": "Programming logic files"
    },
    "STYLE": {
        "extensions": ["css", "scss", "sass", "less", "stylus"],
        "description": "Stylesheet files"
    },
    "CONFIG": {
        "extensions": ["json", "yml", "yaml", "lock", "gitignore", "npmrc", "env"],
        "description": "Configuration files"
    },
    "DOCS": {
        "extensions": ["md", "mdx", "txt", "doc", "docx", "html"],
        "description": "Documentation files"
    }
}

# ===== FILE TYPE MULTIPLIERS =====
# 
# 📊 EXPLANATION OF VALUES:
# 
# Planning Time (hours):
# - LOGIC (1.0h): Complex logic requires understanding context, architecture, side effects
# - STYLE (0.5h): Visual changes need design consideration, but less architectural impact  
# - DOCS (0.3h): Writing requires organization and clarity, but minimal technical complexity
# - CONFIG (0.25h): Usually copy/paste or simple value changes
#
# Implementation Time (hours per line):
# Based on "Mythical Man Month" and modern studies:
# - Industry average: 10-50 lines of debugged code per day (8 hours)
# - This gives us ~0.16-0.8 hours per line for complex code
# - Our values are more optimistic, assuming focused work without meetings/interruptions
#
# LOGIC (0.04h = 2.4min/line): 
#   - Includes thinking, writing, testing, debugging
#   - 25 lines/hour is reasonable for complex logic
#   - Matches empirical data from team observations
#
# STYLE (0.02h = 1.2min/line):
#   - Visual feedback makes iteration faster
#   - Less complex logic, more trial-and-error
#   - 50 lines/hour is achievable for CSS
#
# CONFIG (0.01h = 0.6min/line):
#   - Mostly copy/paste and value changes
#   - 100 lines/hour for JSON/YAML editing
#
# DOCS (0.015h = 0.9min/line):
#   - Writing speed varies, but ~67 lines/hour for technical docs
#   - Includes research and fact-checking time

FILE_TYPE_MULTIPLIERS = {
    "LOGIC": {
        "extensions": ["js", "ts", "jsx", "tsx"],
        "base_time": {
            "planning": 1.0,        # 1 hour - Complex logic needs deep understanding
            "implementation": 0.04  # 2.4 min/line - Industry standard for debugged code
        }
    },
    "CONFIG": {
        "extensions": ["json", "yml", "yaml", "lock", "gitignore", "npmrc", "env"],
        "base_time": {
            "planning": 0.25,       # 15 min - Simple value changes, minimal planning
            "implementation": 0.01  # 0.6 min/line - Fast copy/paste operations
        }
    },
    "STYLE": {
        "extensions": ["css", "scss", "sass", "less", "stylus"],
        "base_time": {
            "planning": 0.5,        # 30 min - Visual design consideration needed
            "implementation": 0.02  # 1.2 min/line - Visual feedback speeds iteration
        }
    },
    "DOCS": {
        "extensions": ["md", "mdx", "txt", "doc", "docx", "html"],
        "base_time": {
            "planning": 0.3,        # 18 min - Organization and structure planning
            "implementation": 0.015 # 0.9 min/line - Technical writing with research
        }
    }
}

# ===== COMMIT TYPE MULTIPLIERS =====
#
# 📊 EXPLANATION OF COMMIT TYPE MULTIPLIERS:
#
# FEATURE (1.0 = 100%): 
#   - New functionality requires full planning and implementation
#   - Base case for time estimation
#   - Includes research, design, coding, testing
#
# FIX (0.5 = 50%):
#   - Bug fixes usually have defined scope
#   - Problem is already identified, solution is more focused
#   - Less planning needed, more targeted implementation
#   - Empirical data shows fixes take ~half the time of features
#
# PUBLISH (0.1 = 10%):
#   - Version bumps, releases are mostly automated
#   - Minimal code changes, mostly configuration
#   - Time spent on verification and deployment
#
# MERGE (0.0 = 0%):
#   - Automated Git operations
#   - No actual development work
#   - Time already counted in the original commits being merged
#
# DEFAULT (0.8 = 80%):
#   - Catch-all for unclear commit messages
#   - Conservative estimate, slightly less than feature
#   - Accounts for commits that might be refactoring or minor changes

COMMIT_TYPE_MULTIPLIERS = {
    "FEATURE": {
        "name": "FEATURE",
        "multiplier": 1.0,      # 100% - Full development cycle
        "patterns": [
            r"^feat:",
            r"^v?\d+\.\d+\.\d+.*\s+-\s+.*feature",
            r"^.*first commit.*mvp"
        ]
    },
    "FIX": {
        "name": "FIX", 
        "multiplier": 0.5,      # 50% - Focused problem solving
        "patterns": [
            r"^fix:",
            r"^v?\d+\.\d+\.\d+.*\s+-\s+.*fix"
        ]
    },
    "PUBLISH": {
        "name": "PUBLISH",
        "multiplier": 0.1,      # 10% - Mostly automated processes
        "patterns": [
            r"^release\/v\d+",
            r"^v?\d+\.\d+\.\d+\s*$",
            r"^Publish\s+v?\d+\.\d+\.\d+$",
            r"^New Release:"
        ]
    },
    "MERGE": {
        "name": "MERGE",
        "multiplier": 0.0,      # 0% - No additional development work
        "patterns": [
            r"^Merge"
        ]
    },
    "DEFAULT": {
        "name": "DEFAULT",
        "multiplier": 0.8       # 80% - Conservative estimate for unclear commits
    }
}

# ===== COMPLEXITY THRESHOLDS =====

COMPLEXITY_THRESHOLDS = {
    "STRUCTURAL": {
        "TRIVIAL": {"max_score": 10, "multiplier": 0.5},     # Very simple changes
        "BASIC": {"max_score": 30, "multiplier": 0.8},       # Basic changes
        "MODERATE": {"max_score": 60, "multiplier": 1.2},    # Moderate changes
        "COMPLEX": {"max_score": 100, "multiplier": 1.6},    # Complex changes
        "VERY_COMPLEX": {"max_score": float('inf'), "multiplier": 2.0}  # Very complex changes
    },
    "ALGORITHMIC": {
        "TRIVIAL": {"max_score": 10, "multiplier": 0.5},     # Very simple changes
        "BASIC": {"max_score": 30, "multiplier": 1.0},       # Basic changes
        "MODERATE": {"max_score": 60, "multiplier": 1.5},    # Moderate changes
        "COMPLEX": {"max_score": 100, "multiplier": 2.0},    # Complex changes
        "VERY_COMPLEX": {"max_score": float('inf'), "multiplier": 2.5}  # Very complex changes
    }
}

# ===== STRUCTURAL PATTERNS =====

STRUCTURAL_PATTERNS = [
    "/components/",
    "/layouts/", 
    "/pages/",
    "/views/",
    "/styles/",
    "/assets/",
    "/themes/"
]

# File types that indicate structural work
STRUCTURAL_FILE_TYPES = ["css", "scss", "less", "html", "jsx", "tsx", "svg"]

# ===== ALGORITHMIC PATTERNS =====

ALGORITHMIC_PATTERNS = [
    "/utils/",
    "/helpers/",
    "/services/",
    "/hooks/",
    "/commands/",
    "/lib/",
    "/core/"
]

# File types that indicate algorithmic work
ALGORITHMIC_FILE_TYPES = ["js", "ts", "jsx", "tsx"]

# ===== TIME CALCULATION FACTORS =====
#
# 📊 EXPLANATION OF TIME FACTORS:
#
# PLANNING_BASE (0.3 = 30%):
#   - Minimum planning time as percentage of base time
#   - Even simple changes need some thinking
#   - Based on observation that ~30% of development time is planning
#
# PLANNING_NET_WEIGHT (0.7 = 70%):
#   - Additional planning weight for net additions
#   - More new code = more planning needed
#   - Formula: planning = base * (0.3 + net_ratio * 0.7)
#   - Net additions get full planning, deletions get reduced planning
#
# PLANNING_DELETION_FACTOR (0.2 = 20%):
#   - When deletions > additions, reduce planning time to 20%
#   - Removing code requires less planning than adding
#   - You already know what needs to be removed
#
# DELETION_TIME_FACTOR (0.1 = 10%):
#   - Deleting code takes 10% of the time vs writing it
#   - Deletion is faster: find code, verify dependencies, remove
#   - Writing requires thinking, testing, documentation

# Planning time factors
PLANNING_BASE = 0.3                 # 30% minimum planning time
PLANNING_NET_WEIGHT = 0.7           # 70% additional weight for net additions  
PLANNING_DELETION_FACTOR = 0.2      # 20% planning time when mostly deletions

# Implementation time factors
DELETION_TIME_FACTOR = 0.1          # 10% time for deletions vs additions

# ===== COMPLEXITY SCORING WEIGHTS =====
#
# 📊 EXPLANATION OF SCORING WEIGHTS:
#
# These values determine how complexity scores are calculated.
# Higher scores = higher complexity multipliers = more time estimated.
#
# STRUCTURAL SCORING:
# - pattern_match (10): Each /components/, /styles/ etc. adds 10 points
# - file_type_match (5): Each .css, .scss file adds 5 points  
# - files_changed (2): Each file changed adds 2 points
# - style_files (8): Extra points for CSS files (visual iteration)
#
# ALGORITHMIC SCORING:
# - pattern_match (15): Each /utils/, /services/ etc. adds 15 points (higher than structural)
# - file_type_match (8): Each .js, .ts file adds 8 points
# - avg_lines_divisor (10): Average lines per file divided by 10
# - max_avg_lines_score (20): Cap the lines score at 20 points
# - deletion_ratio_weight (5): Deletion ratio * 5 points
# - max_deletion_ratio (1.5): Cap deletion ratio at 1.5x
#
# Score ranges typically:
# - 0-10: TRIVIAL (0.5x multiplier)
# - 11-30: BASIC (0.8x or 1.0x multiplier)  
# - 31-60: MODERATE (1.2x or 1.5x multiplier)
# - 61-100: COMPLEX (1.6x or 2.0x multiplier)
# - 100+: VERY_COMPLEX (2.0x or 2.5x multiplier)

COMPLEXITY_SCORING = {
    "STRUCTURAL": {
        "pattern_match": 10,        # Points per /components/, /styles/ match
        "file_type_match": 5,       # Points per .css, .scss file
        "files_changed": 2,         # Points per file in commit
        "style_files": 8            # Extra points for visual iteration files
    },
    "ALGORITHMIC": {
        "pattern_match": 15,        # Points per /utils/, /services/ match (higher complexity)
        "file_type_match": 8,       # Points per .js, .ts file
        "avg_lines_divisor": 10,    # Divide avg lines by this for score
        "max_avg_lines_score": 20,  # Cap lines contribution at 20 points
        "deletion_ratio_weight": 5, # Multiply deletion ratio by this
        "max_deletion_ratio": 1.5   # Cap deletion ratio at 1.5x
    }
}

# ===== HELPER FUNCTIONS =====

def get_file_extension(filename: str) -> str:
    """
    Extract file extension from filename.
    
    Handles special cases like .stories.tsx, .test.ts, etc.
    Returns the actual extension (ts, tsx) not the special prefix.
    
    Args:
        filename: The filename to analyze
        
    Returns:
        The file extension or 'unknown' if not found
    """
    import re
    
    # Check for special patterns like .stories.tsx or .test.ts
    special_match = re.search(r'\.(stories|test|spec)\.([a-zA-Z0-9]+)(?:\})?$', filename)
    if special_match:
        return special_match.group(2)  # Return the actual extension
    
    # Get base extension
    base_match = re.search(r'\.([a-zA-Z0-9]+)(?:\})?$', filename)
    if base_match:
        return base_match.group(1)
    
    return 'unknown'


def get_file_category(file_type: str) -> Dict[str, Any]:
    """
    Get file category and base time for a given file type.
    
    Args:
        file_type: The file extension
        
    Returns:
        Dictionary with category name and base time information
    """
    for category, info in FILE_TYPE_MULTIPLIERS.items():
        if file_type in info["extensions"]:
            return {
                "category": category,
                "base_time": info["base_time"]
            }
    
    # Default to LOGIC if unknown
    return {
        "category": "LOGIC",
        "base_time": FILE_TYPE_MULTIPLIERS["LOGIC"]["base_time"]
    }


def get_commit_type(message: str) -> str:
    """
    Determine commit type from commit message.
    
    Args:
        message: The commit message
        
    Returns:
        The commit type name
    """
    import re
    
    # Check each commit type pattern
    for commit_type, info in COMMIT_TYPE_MULTIPLIERS.items():
        if commit_type == "DEFAULT":
            continue
            
        for pattern in info["patterns"]:
            if re.match(pattern, message, re.IGNORECASE):
                return commit_type
    
    return "DEFAULT"


def get_complexity_level(score: float, complexity_type: str) -> str:
    """
    Determine complexity level based on score and type.
    
    Args:
        score: The calculated complexity score
        complexity_type: Either 'STRUCTURAL' or 'ALGORITHMIC'
        
    Returns:
        The complexity level name
    """
    thresholds = COMPLEXITY_THRESHOLDS[complexity_type]
    
    for level, info in thresholds.items():
        if score <= info["max_score"]:
            return level
    
    return "VERY_COMPLEX"


def get_complexity_multiplier(complexity_type: str, complexity_level: str) -> float:
    """
    Get complexity multiplier for given type and level.
    
    Args:
        complexity_type: Either 'STRUCTURAL' or 'ALGORITHMIC'
        complexity_level: The complexity level
        
    Returns:
        The multiplier value
    """
    return COMPLEXITY_THRESHOLDS[complexity_type][complexity_level]["multiplier"]


# ===== EXPORT ALL CONSTANTS =====

__all__ = [
    # File categories (from files.py)
    "FILE_CATEGORIES",
    
    # Main constants
    "FILE_TYPE_MULTIPLIERS",
    "COMMIT_TYPE_MULTIPLIERS", 
    "COMPLEXITY_THRESHOLDS",
    "STRUCTURAL_PATTERNS",
    "ALGORITHMIC_PATTERNS",
    "STRUCTURAL_FILE_TYPES",
    "ALGORITHMIC_FILE_TYPES",
    
    # Time factors
    "PLANNING_BASE",
    "PLANNING_NET_WEIGHT", 
    "PLANNING_DELETION_FACTOR",
    "DELETION_TIME_FACTOR",
    
    # Scoring weights
    "COMPLEXITY_SCORING",
    
    # Helper functions
    "get_file_extension",
    "get_file_category",
    "get_commit_type",
    "get_complexity_level",
    "get_complexity_multiplier"
]
